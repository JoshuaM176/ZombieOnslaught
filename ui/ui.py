import pygame as pg

class UI:

    def __init__(self, screen: pg.display):
        self.screen = screen
        self.render_plain = pg.sprite.RenderPlain
        self.properties = {"player": {"health": 0, "experience": 0}, "loadout": {"weapon": None, "ammo": 0}, "level": {"round": 0}}

    def update(self, category: str):
        pass

    def remove(self):
        pass

    def update(self):
        pass