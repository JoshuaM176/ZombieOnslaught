import pygame as pg
from entities.bullets import Bullet, Tracer

class TracerRegistry:

    def __init__(self, length: int, screen: pg.display):
        self.screen = screen
        self.length = length
        self.tracers: list[Tracer] = [None] * self.length
        self.index = 0

    def register(self, tracer: Tracer):
        self.tracers[self.index] = tracer
        self.index += 1
        if self.index >= self.length:
            self.index = 0

    def update(self):
        surface = pg.Surface(self.screen.get_size(), pg.SRCALPHA)
        for tracer in self.tracers:
            if tracer is not None:
                if tracer.vis > 0:
                    pg.draw.line(surface, *tracer.update())
        self.screen.blit(surface, (0,0))


class BulletRegistry:
    
    def __init__(self, tracer_registry: TracerRegistry, length: int):
        self.tracer_registry = tracer_registry
        self.length = length
        self.bullets: list[Bullet] = [None] * self.length
        self.index = 0

    def register(self, bullet: Bullet):
        self.bullets[self.index] = bullet
        self.index += 1
        if self.index >= self.length:
            self.index = 0

    def get(self):
        for bullet in self.bullets:
            if bullet is not None:
                if bullet.x > -100 and bullet.x < 3000 and bullet.y > -100 and bullet.y < 1500 and bullet.damage > 0:
                    yield bullet

    def update(self):
        for bullet in self.bullets:
            if bullet is not None:
                if bullet.x > -100 and bullet.x < 3000 and bullet.y > -500 and bullet.y < 1500 and bullet.damage > 0:
                    if bullet.tracer == True:
                        self.tracer_registry.register(Tracer(*bullet.update()))
                    else: bullet.update()
        self.tracer_registry.update()

