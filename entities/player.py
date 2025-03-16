import math
import pygame as pg
from registries.weapon_registry import WeaponRegistry
from registries.bullet_registry import BulletRegistry
from entities.entity import Entity

class Player(Entity):
    
    def __init__(self, screen, bullet_registry: BulletRegistry, render_plain: pg.sprite.RenderPlain):
        self.weapons = ["Melee", "SMG"]
        self.index = 0
        resources = {"sprite": "player.png", "speed": 5, "health": 10, "hitbox": [24, 16, 72, 112]}
        Entity.__init__(self, resources, "player", 300, 300)
        self.weapon_registry = WeaponRegistry(pg.sprite.RenderPlain(()), self.weapons)
        self.weapon_registry.load_default_weapons(bullet_registry)
        self.speed = self.weapon_registry.equip(self.weapons[self.index])
        self.render_plain = render_plain
        self.screen = screen
        self.render_plain.add(self)
        self.shooting = False

    def hit(self, damage):
        self.health -= damage

    def update(self):
        self.render_plain.draw(self.screen)

    def process(self, inp: dict):
        #Movement
        mult = math.sqrt((inp["hor"]**2 + inp["ver"]**2))
        if mult != 0:
            speed = self.speed * (inp["sprint"])
            self.posx += speed * inp["hor"]/mult
            self.posy += speed * inp["ver"]/mult
            self.hitbox.update(self.posx, self.posy)
        #Switch weapons
        if inp["eq"] == 1:
            if self.index < len(self.weapons)-1:
                self.index += 1
            type = self.weapons[self.index]
            self.speed = self.weapon_registry.equip(type)
            inp["eq"] = 0
        if inp["eq"] == -1:
            if self.index > 0:
                self.index -=1
            type = self.weapons[self.index]
            self.speed = self.weapon_registry.equip(type)
            inp["eq"] = 0
        #Shooting
        if inp["shooting"] == 1:
            self.shooting = True
        else: self.shooting = False
        self.rect.topleft = (self.posx, self.posy)
        self.render_plain.update()
        self.weapon_registry.update(self.screen, self.posx, self.posy, self.shooting)
        
        