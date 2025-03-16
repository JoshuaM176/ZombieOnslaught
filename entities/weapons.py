import pygame as pg
from resources.resource_loader.resource_loader import ResourceLoader
from entities.bullets import Bullet
from registries.bullet_registry import BulletRegistry
from resources.resources import load_sprite
import random as rand

weapon_loader = ResourceLoader('weapons')
weapon_loader.load_all()

class Weapon(pg.sprite.Sprite):

    def __init__(self, bullet_registry: BulletRegistry, attributes = "", colorkey = -1, resources = None):
        #load weapon
        pg.sprite.Sprite.__init__(self)
        self.bullet_registry = bullet_registry
        default = weapon_loader.get('default')
        if resources == None:
            resources = weapon_loader.get(attributes)
        resources = weapon_loader.update(default, resources)
        
        self.weapon = resources['weapon']
        self.image, self.rect = load_sprite(self.weapon['sprite'], 'weapons', colorkey)
        self.player = resources['player']
        self.bullet = resources["bullet"]
        self.recoil = resources["weapon"]["recoil"]
        self.ver = 0

        #set defaults
        if self.bullet.get('tracer') == "false":
            self.bullet['tracer'] = False
        else:
            self.bullet['tracer'] = True
        self.weapon['shiftX'] = self.weapon.get('shiftX') or 0
        self.weapon['shiftY'] = self.weapon.get('shiftY') or 0
        
        self.clock = 0
        self.ticksToFire = 3600/self.weapon['firerate']
    
    def update_recoil(self, shoot: bool, recoil: float, recoil_control: float, max_recoil: float):
        if shoot:
            self.ver += recoil
            if self.ver > max_recoil:
                self.ver = max_recoil
        elif self.ver > 0:
            self.ver -= recoil_control
            if self.ver < 0:
                self.ver = 0

    def shoot(self, x: int, y: int):
        self.bullet["x"] = x + self.bullet["shiftX"]
        self.bullet["y"] = y + self.bullet["shiftY"]
        self.bullet_registry.register(Bullet(**self.bullet, hor = 20, ver = -self.ver + rand.normalvariate(0, 0.1), color = self.bullet.get('color') or (250, 250, 0)))

    def update(self, pX, pY, shoot):
        x = pX + self.weapon["shiftX"]
        y = pY + self.weapon["shiftY"]
        if self.clock < self.ticksToFire:
            self.clock+=1
        if shoot and self.clock >= self.ticksToFire:
            self.clock -= self.ticksToFire
            self.shoot(x, y)
        self.update_recoil(shoot, **self.recoil)
        self.rect.topleft = (x, y)