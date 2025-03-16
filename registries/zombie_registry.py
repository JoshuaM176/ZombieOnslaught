import pygame as pg
from entities.zombies import Zombie

class ZombieRegistry:
    def __init__(self, render_plain: pg.sprite.RenderPlain):
        self.zombies: list[Zombie] = []
        self.render_plain = render_plain

    def register(self, zombie: Zombie):
        self.zombies.append(zombie)
        self.render_plain.add(zombie)

    def deregister(self, zombie: Zombie):
        self.zombies.remove(zombie)
        self.render_plain.remove(zombie)

    def end_of_frame(self):
        for zombie in self.zombies:
            if zombie.posx < -100:
                self.deregister(zombie)
            elif zombie.health < 0:
                self.deregister(zombie)

    def update(self, screen: pg.display):
        self.render_plain.update(screen)
        self.render_plain.draw(screen)

    def get(self) -> list[Zombie]:
        return self.zombies

    def isEmpty(self):
        if len(self.zombies) > 0:
            return False
        return True