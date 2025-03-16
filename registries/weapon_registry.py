import pygame as pg
from entities.weapons import Weapon

class WeaponRegistry:
    
    def __init__(self, render_plain: pg.sprite.RenderPlain):
        self.weapon_classes = ["Melee", "SMG", "Pistol", "Rifle", "Shotgun", "Sniper"]
        self.weapons: dict[str: Weapon] = {}
        for weapon in self.weapon_classes:
            self.weapons[weapon] = None
        self.render_plain = render_plain
        self.index = 1

    def __equip__(self, type):
        self.render_plain.add(self.weapons[type])

    def deregister(self, type: str):
        self.weapons[type] = None

    def register(self, type: str, weapon: Weapon):
        self.weapons[type] = weapon

    def next(self):
        if self.index < len(self.weapon_classes)-1:
            self.render_plain.remove(self.weapons[self.weapon_classes[self.index]])
            self.index +=1
            self.__equip__(self.weapon_classes[self.index])
        return self.weapons[self.weapon_classes[self.index]].movement

    def previous(self):
        if self.index > 0:
            self.render_plain.remove(self.weapons[self.weapon_classes[self.index]])
            self.index -=1
            self.__equip__(self.weapon_classes[self.index])
        return self.weapons[self.weapon_classes[self.index]].movement
    
    def update(self, screen: pg.display, pX: int, pY: int, shoot: bool):
        self.render_plain.update(pX, pY, shoot)
        self.render_plain.draw(screen)

    def load_default_weapons(self, bullet_registry):
        self.register("SMG", Weapon("mp7", bullet_registry))
        self.__equip__("SMG")
        self.register("Melee", Weapon("chainsaw", bullet_registry))