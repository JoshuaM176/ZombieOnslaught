import pygame as pg
from resources.resource_loader.resource_loader import ResourceLoader
from entities.bullets import Bullet
from registries.bullet_registry import BulletRegistry
from resources.resources import load_sprite

weapon_loader = ResourceLoader('weapons')
weapon_loader.load_all()

class Weapon(pg.sprite.Sprite):

    def __init__(self, bullet_registry: BulletRegistry, attributes = "", colorkey = -1, resources = None):
        #load weapon
        pg.sprite.Sprite.__init__(self)
        self.bullet_registry = bullet_registry
        if resources == None:
            resources = self.get_resources(attributes)
        self.weapon = resources['weapon']
        self.image, self.rect = load_sprite(self.weapon['sprite'], 'weapons', colorkey)
        self.player = resources['player']
        self.bullet = resources["bullet"]

        #set defaults
        if self.bullet.get('tracer') == "false":
            self.bullet['tracer'] = False
        else:
            self.bullet['tracer'] = True
        self.weapon['shiftX'] = self.weapon.get('shiftX') or 0
        self.weapon['shiftY'] = self.weapon.get('shiftY') or 0

        
        self.clock = 0
        self.ticksToFire = 3600/self.weapon['firerate']

    def get_resources(self, attributes: str) -> dict:
        resources = weapon_loader.get(attributes)
        return resources

    def shoot(self, x: int, y: int):
        self.bullet["x"] = x + self.bullet["shiftX"]
        self.bullet["y"] = y + self.bullet["shiftY"]
        self.bullet_registry.register(Bullet(**self.bullet, hor = 15, ver = 1, color = self.bullet.get('color') or (250, 250, 0)))

    def update(self, pX, pY, shoot):
        x = pX + self.weapon["shiftX"]
        y = pY + self.weapon["shiftY"]
        if self.clock < self.ticksToFire:
            self.clock+=1
        if shoot and self.clock >= self.ticksToFire:
            self.clock -= self.ticksToFire
            self.shoot(x, y)
        self.rect.topleft = (x, y)