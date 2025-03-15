import pygame as pg
from resources.resources import load_sprite
from resources.resource_loader.resource_loader import ResourceLoader
from entities.hitbox import HitBox

zombie_loader = ResourceLoader('zombies')
zombie_loader.load_all()

class Zombie(pg.sprite.Sprite):

    def __init__(self, attributes: str, colorkey = -1):
        pg.sprite.Sprite.__init__(self)
        resources = zombie_loader.get(attributes)
        sprite = resources.get('sprite') or 'zombie.png'
        self.image, self.rect = load_sprite(sprite, 'zombies', colorkey)
        self.speed = resources.get('speed') or 5
        self.health = resources.get('health') or 10
        self.posx = 1000
        self.posy = 200
        self.hitbox = HitBox(self.posx, self.posy, *resources.get('hitbox'))

    def hit(self, damage):
        self.health -= damage

    def update(self):
        self.posx -= self.speed
        self.hitbox.update(self.posx, self.posy)
        self.rect.topleft = (self.posx, self.posy)



        

