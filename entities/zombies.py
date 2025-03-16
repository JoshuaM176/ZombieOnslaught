import pygame as pg
from resources.resource_loader.resource_loader import ResourceLoader
from entities.entity import Entity
from registries.weapon_registry import WeaponRegistry
from registries.bullet_registry import BulletRegistry
from entities.weapons import Weapon

zombie_loader = ResourceLoader('zombies')
zombie_loader.load_all()

weapon_loader = ResourceLoader('weapons')
weapon_loader.load_all()

class Zombie(Entity):

    def __init__(self, attributes: str, x: int, y: int, bullet_registry: BulletRegistry):
        resources = zombie_loader.get(attributes)
        Entity.__init__(self, resources, 'zombies', x, y)
        self.weapon_registry = WeaponRegistry(pg.sprite.RenderPlain(()), ["Fist"])
        weapon_resources = weapon_loader.get(resources["weapon"])
        self.weapon = Weapon(bullet_registry, resources = weapon_resources)
        self.weapon_registry.register("Fist", self.weapon)
        self.weapon_registry.equip("Fist", 0)

    def hit(self, damage):
        self.health -= damage

    def update_weapon(self, screen):
        self.weapon_registry.update(screen, self.posx, self.posy, True)

    def update(self):
        self.posx -= self.speed
        self.hitbox.update(self.posx, self.posy)
        self.rect.topleft = (self.posx, self.posy)



        

