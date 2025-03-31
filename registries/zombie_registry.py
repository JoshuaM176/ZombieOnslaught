import pygame as pg
from entities.zombies import Zombie
from entities.entity import Entity
from game.ui import UI

class EntityRegistry:
    def __init__(self, render_plain: pg.sprite.RenderPlain, ui: UI):
        self.ui = ui
        self.entities: list[Entity] = []
        self.render_plain = render_plain

    def register(self, entity: Entity):
        self.entities.append(entity)
        self.render_plain.add(entity)

    def deregister(self, entity: Entity):
        self.entities.remove(entity)
        self.render_plain.remove(entity)

    def update(self, screen: pg.display):
        self.render_plain.update()
        self.render_plain.draw(screen)

    def get(self):
        return self.entities
    
    def isEmpty(self):
        if len(self.entities) > 0:
            return False
        return True

class ZombieRegistry(EntityRegistry):
    def __init__(self, render_plain: pg.sprite.RenderPlain, ui: UI):
        super().__init__(render_plain, ui)
        self.entities: list[Zombie] = []

    def register(self, zombie: Zombie):
        super().register(zombie)

    def deregister(self, zombie: Zombie):
        super().deregister(zombie)

    def end_of_frame(self):
        for zombie in self.entities:
            if zombie.posx < -100:
                self.deregister(zombie)
            elif zombie.health < 0:
                self.deregister(zombie)

    def update(self, screen: pg.display):
        super().update(screen)
        self.send_to_ui()
        for zombie in self.entities:
            zombie.update_weapon(screen)

    def send_to_ui(self):
        info = []
        for zombie in self.entities:
            toAdd = {"max_health": zombie.max_health, "health": zombie.health, "x": zombie.posx, "y": zombie.posy, "shiftX": zombie.uiShiftX}
            info.append(toAdd)
        self.ui.send({"zombies": info})