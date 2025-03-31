import pygame as pg
from resources.resource_loader.resource_loader import ResourceLoader
from entities.entity import Entity
from registries.weapon_registry import WeaponRegistry
from registries.bullet_registry import BulletRegistry
from entities.weapons import Weapon

zombie_loader = ResourceLoader('zombies', 'attributes')
zombie_loader.load_all()

weapon_loader = ResourceLoader('weapons', 'attributes')
weapon_loader.load_all()

class Zombie(Entity):

    def __init__(self, attributes: str, x: int, y: int, bullet_registry: BulletRegistry, difficulty: int):
        default = zombie_loader.get("default")
        resources = zombie_loader.get(attributes)
        resources = zombie_loader.update(default, resources)
        resources["health"] *= (1+difficulty/100)
        resources["speed"] *= (1+difficulty/200)
        Entity.__init__(self, resources, 'zombies', x, y)
        self.weapon_registry = WeaponRegistry(pg.sprite.RenderPlain(()), ["Default"])
        self.weapon_resources = weapon_loader.get(resources["weapon"])
        self.weapon = Weapon(bullet_registry, resources = self.weapon_resources)
        self.weapon_registry.register("Default", self.weapon)
        self.weapon_registry.equip("Default")

    def hit(self, damage):
        self.health -= damage

    def update_weapon(self, screen):
        self.weapon_registry.update(screen, self.posx, self.posy, True, False)

    def update(self):
        self.posx -= self.speed
        self.hitbox.update(self.posx, self.posy)
        self.rect.topleft = (self.posx, self.posy)



        

