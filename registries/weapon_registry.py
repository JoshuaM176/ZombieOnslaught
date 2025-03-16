import pygame as pg
from entities.weapons import Weapon

class WeaponRegistry:
    
    def __init__(self, render_plain: pg.sprite.RenderPlain, weapon_classes: list[str]):
        self.weapon_classes = weapon_classes
        self.weapons: dict[str: Weapon] = {}
        for weapon in self.weapon_classes:
            self.weapons[weapon] = None
        self.render_plain = render_plain
        self.index = 0

    def equip(self, type, index):
        self.index = index
        self.render_plain.add(self.weapons[type])

    def deregister(self, type: str):
        self.weapons[type] = None

    def register(self, type: str, weapon: Weapon):
        self.weapons[type] = weapon

    def next(self):
        if self.index < len(self.weapon_classes)-1:
            self.render_plain.remove(self.weapons[self.weapon_classes[self.index]])
            index = self.index+1
            self.equip(self.weapon_classes[index], index)
        return self.get_equipped().player['movement']

    def previous(self):
        if self.index > 0:
            self.render_plain.remove(self.weapons[self.weapon_classes[self.index]])
            index = self.index-1
            self.equip(self.weapon_classes[index], index)
        return self.get_equipped().player['movement']
    
    def get_equipped(self) -> Weapon:
        return self.weapons[self.weapon_classes[self.index]]
    
    def update(self, screen: pg.display, eX: int, eY: int, shoot: bool):
        self.render_plain.update(eX, eY, shoot)
        self.render_plain.draw(screen)

    def load_default_weapons(self, bullet_registry):
        self.register("SMG", Weapon(bullet_registry, "mp7"))
        self.register("Melee", Weapon(bullet_registry, "chainsaw"))
        self.equip("Melee", 0)

    def load_weapon(self, weapon_class: str, weapon: str, bullet_registry):
        self.register(weapon_class, Weapon(bullet_registry, weapon))