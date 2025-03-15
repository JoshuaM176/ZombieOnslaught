import pygame as pg
from resources.resource_loader.resource_loader import ResourceLoader
from entities.bullets import Bullet
from registries.bullet_registry import BulletRegistry
from resources.resources import load_sprite

weapon_loader = ResourceLoader('weapons')
weapon_loader.load_all()

class Weapon(pg.sprite.Sprite):

    def __init__(self, attributes: str, bullet_registry: BulletRegistry, colorkey = -1):
        pg.sprite.Sprite.__init__(self)
        self.bullet_registry = bullet_registry
        resources = weapon_loader.get(attributes)
        sprite = resources.get('sprite') or 'mp7'
        self.image, self.rect = load_sprite(sprite, 'weapons', colorkey)
        self.movement = resources.get('movement') or 5
        self.damage = resources.get('damage') or 10
        self.firerate = resources.get('firerate') or 600
        self.dropoff = resources.get('dropoff') or 1
        self.velocity = resources.get('velocity') or 25
        self.penetration = resources.get('penetration') or 0.1
        self.shiftX = resources.get("shiftX") or 0
        self.shiftY = resources.get("shiftY") or 0
        self.bShiftX = resources.get("bShiftX") or 0
        self.bShiftY = resources.get("bShiftY") or 0
        self.clock = 0
        self.ticksToFire = 3600/self.firerate

    def shoot(self, x: int, y: int):
        self.bullet_registry.register(Bullet(x + self.bShiftX, y + self.bShiftY, 15, 1, 25, self.damage, self.dropoff, self.penetration))

    def update(self, pX, pY, shoot):
        x = pX + self.shiftX
        y = pY + self.shiftY
        if self.clock < self.ticksToFire:
            self.clock+=1
        if shoot and self.clock >= self.ticksToFire:
            self.clock -= self.ticksToFire
            self.shoot(x, y)
        self.rect.topleft = (x, y)