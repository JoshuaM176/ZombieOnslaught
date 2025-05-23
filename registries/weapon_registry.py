import pygame as pg
from entities.weapons import Weapon

class WeaponRegistry:
    
    def __init__(self, render_plain: pg.sprite.RenderPlain, weapon_classes: list[str], ui = None):
        self.ui = ui
        self.weapons: dict[str: Weapon] = {}
        for weapon in weapon_classes:
            self.weapons[weapon] = None
        self.render_plain = render_plain
        self.equipped = None

    def equip(self, type: str) -> int:
        if self.get_equipped() != None:
            self.render_plain.remove(self.get_equipped())
        self.render_plain.add(self.weapons[type])
        self.equipped = type
        return self.weapons[type].player['movement']
        
    def deregister(self, type: str):
        self.weapons[type] = None

    def register(self, type: str, weapon: Weapon):
        self.weapons[type] = weapon
    
    def get_equipped(self) -> Weapon:
        if self.equipped != None:
            return self.weapons[self.equipped]
        return None
    
    def update(self, screen: pg.display, eX: int, eY: int, shoot: bool, reload: bool):
        self.render_plain.update(eX, eY, shoot, reload)
        self.render_plain.draw(screen)
        if self.get_return() is not None:
            return self.get_return()
        return shoot
    
    def get_return(self):
        return self.get_equipped().rtn

    def load_default_weapons(self, bullet_registry):
        self.register("SMG", Weapon(bullet_registry, "MP7", self.ui))
        self.register("Melee", Weapon(bullet_registry, "Chainsaw", self.ui))
        self.equip("Melee")

    def load_weapon(self, weapon_class: str, weapon: str, bullet_registry):
        self.register(weapon_class, Weapon(bullet_registry, weapon))