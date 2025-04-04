import pygame as pg
from resources.resources import load_sprite
from entities.hitbox import HitBox

class Entity(pg.sprite.Sprite):

    def __init__(self, resources: dict, category: str, x, y, colorkey = -1):
        pg.sprite.Sprite.__init__(self)
        self.sprite = resources.get('sprite') or 'zombie.png'
        self.image, self.rect = load_sprite(self.sprite, category, colorkey)
        self.speed = resources.get('speed') or 5
        self.max_health = resources.get('health')
        self.health = resources.get('health') or 10
        self.uiShiftX = resources.get('uiShiftX') or 0
        self.posx = x
        self.posy = y
        self.hitbox = HitBox(self.posx, self.posy, *resources.get('hitbox'))
        self.head_hitbox = HitBox(self.posx, self.posy, *resources.get('head_hitbox'))

    def hit():
        pass
    