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
        self.weapon_registry = WeaponRegistry(pg.sprite.RenderPlain(()), ["None"])
        weapon_resources = weapon_loader.get(resources["weapon"])
        self.weapon = Weapon(bullet_registry, resources["weapon"])
        self.weapon_registry.register("None", self.weapon)
        self.weapon_registry.equip("None", 0)


    def hit(self, damage):
        self.health -= damage

    def update(self, screen):
        self.posx -= self.speed
        self.hitbox.update(self.posx, self.posy)
        self.weapon_registry.update(screen, self.posx, self.posy, True)
        self.rect.topleft = (self.posx, self.posy)



        

