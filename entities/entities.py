import pygame as pg
import math
from resources.resources import load_sprite

class Zombie(pg.sprite.Sprite):

    def __init__(self, sprite, attributes: str, colorkey = -1):
        pg.sprite.Sprite.__init__(self)
        self.image, self.rect = load_sprite(sprite, colorkey, scale=8)
        self.posx = 1000
        self.posy = 200
        self.speed = 10
        self.health = 10

    def update(self):
        self.posx -= self.speed
        self.rect.topleft = (self.posx, self.posy)


class Player(pg.sprite.Sprite):
    
    def __init__(self, colorkey = -1):
        pg.sprite.Sprite.__init__(self)
        self.image, self.rect = load_sprite('player.png', colorkey, scale=8)
        self.posx = 300
        self.posy = 300
        self.speed = 5

    def update(self, inp: dict):
        mult = math.sqrt((inp["hor"]**2 + inp["ver"]**2))
        if mult != 0:
            speed = self.speed * (inp["sprint"])
            self.posx += speed * inp["hor"]/mult
            self.posy += speed * inp["ver"]/mult
        self.rect.topleft = (self.posx, self.posy)

