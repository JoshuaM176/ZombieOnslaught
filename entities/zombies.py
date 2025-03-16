import pygame as pg
from resources.resources import load_sprite
from resources.resource_loader.resource_loader import ResourceLoader
from entities.hitbox import HitBox
from entities.entity import Entity

zombie_loader = ResourceLoader('zombies')
zombie_loader.load_all()

class Zombie(Entity):

    def __init__(self, attributes: str, x: int, y: int, colorkey = -1):
        resources = zombie_loader.get(attributes)
        Entity.__init__(self, attributes, resources, 'zombies', x, y)

    def hit(self, damage):
        self.health -= damage

    def update(self):
        self.posx -= self.speed
        self.hitbox.update(self.posx, self.posy)
        self.rect.topleft = (self.posx, self.posy)



        

