import math
import pygame as pg
from resources.resources import load_sprite
from registries.weapon_registry import WeaponRegistry

class Player(pg.sprite.Sprite):
    
    def __init__(self, screen, weapon_registry: WeaponRegistry, render_plain: pg.sprite.RenderPlain, colorkey = -1):
        pg.sprite.Sprite.__init__(self)
        self.weapon_registry = weapon_registry
        self.render_plain = render_plain
        self.screen = screen
        self.image, self.rect = load_sprite('player.png', 'player', colorkey)
        self.render_plain.add(self)
        self.posx = 300
        self.posy = 300
        self.speed = 5
        self.shooting = False

    def update(self):
        self.render_plain.draw(self.screen)


    def process(self, inp: dict):
        #Movement
        mult = math.sqrt((inp["hor"]**2 + inp["ver"]**2))
        if mult != 0:
            speed = self.speed * (inp["sprint"])
            self.posx += speed * inp["hor"]/mult
            self.posy += speed * inp["ver"]/mult
        #Switch weapons
        if inp["eq"] == 1:
            self.speed = self.weapon_registry.next()
            inp["eq"] = 0
        if inp["eq"] == -1:
            self.speed = self.weapon_registry.previous()
            inp["eq"] = 0
        #Shooting
        if inp["shooting"] == 1:
            self.shooting = True

        else: self.shooting = False
        self.rect.topleft = (self.posx, self.posy)
        self.render_plain.update()
        self.weapon_registry.update(self.screen, self.posx, self.posy, self.shooting)
        
        