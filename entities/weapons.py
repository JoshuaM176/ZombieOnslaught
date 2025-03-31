import pygame as pg
from resources.resource_loader.resource_loader import ResourceLoader
from entities.bullets import Bullet
from registries.bullet_registry import BulletRegistry
from resources.resources import load_sprite
from game.ui import UI
import random as rand

weapon_loader = ResourceLoader('weapons', 'attributes')
weapon_loader.load_all()

class Weapon(pg.sprite.Sprite):

    def __init__(self, bullet_registry: BulletRegistry, attributes = "", ui = None, colorkey = -1, resources = None):
        self.ui = ui
        self.name = attributes
        #load weapon
        pg.sprite.Sprite.__init__(self)
        self.bullet_registry = bullet_registry
        default = weapon_loader.get('default')
        if resources == None:
            resources = weapon_loader.get(attributes)
        resources = weapon_loader.update(default, resources)
        self.weapon = resources['weapon']
        self.player = resources['player']
        self.bullet = resources["bullet"]
        self.init_recoil(self.weapon["recoil"])
        self.init_ammo(self.weapon["ammo"])
        self.ver = 0
        self.init_sprites(**resources["weapon"]["sprites"], colorkey = colorkey)
        self.image, self.rect = self.default
        self.rtn = None

        #set defaults
        if self.bullet.get('tracer') == "false":
            self.bullet['tracer'] = False
        else:
            self.bullet['tracer'] = True
        self.weapon['shiftX'] = self.weapon.get('shiftX') or 0
        self.weapon['shiftY'] = self.weapon.get('shiftY') or 0
        
        self.clock = 0
        self.ticksToFire = 3600/self.weapon['firerate']

    def init_sprites(self, default, reloading, extra_reload_sprite, fire_sprite, fire_animation_length, colorkey):
        self.default = load_sprite(default, 'weapons', colorkey)
        self.extra_reload_sprite = load_sprite(extra_reload_sprite, 'weapons', colorkey)
        self.fire_sprite = load_sprite(fire_sprite, 'weapons', colorkey)
        self.fire_animation_time = 0
        self.fire_animation_length = fire_animation_length
        self.reload_sprites = []
        for sprite in reloading:
            self.reload_sprites.append(load_sprite(sprite, 'weapons', colorkey))
        self.time_per_reload_step = self.reload_time/len(self.reload_sprites)

    def init_recoil(self, data):
        for key, value in data.items():
            setattr(self, key, value)

    def init_ammo(self, data):
        for key, value in data.items():
            setattr(self, key, value)
        self.bullets = self.bullets_per_mag
        self.mags = self.max_mags
        self.reload_time = self.reload_time * 60
        self.reload_progress = 0
        self.reloading = False
        if self.bullet_in_chamber == 1:
            self.bic = True
        else:
            self.bic = False
        self.reload_on_empty = self.reload_on_empty*60

    def send_to_ui(self):
        info = {"bullets": self.bullets, "max_bullets": self.bullets_per_mag, "mags": self.mags, "max_mags": self.max_mags, "reload_progress": self.reload_progress/self.reload_time, "reload_time_left": self.reload_time-self.reload_progress, "name": self.name}
        if self.bic:
            info["bullets"] += self.bullet_in_chamber
        if self.ui is not None:
            self.ui.send({"weapon": info})
    
    def update_recoil(self, shoot: bool, recoil: float, recoil_control: float, max_recoil: float):
        if shoot:
            self.ver += recoil
            if self.ver > max_recoil:
                self.ver = max_recoil
        elif self.ver > 0:
            self.ver -= recoil_control
            if self.ver < 0:
                self.ver = 0

    def shoot(self, x: int, y: int):
        self.fire_animation_time = self.fire_animation_length
        self.bullet["x"] = x + self.bullet["shiftX"]
        self.bullet["y"] = y + self.bullet["shiftY"]
        self.bullet_registry.register(Bullet(**self.bullet, hor = 20, ver = -self.ver + rand.normalvariate(0, 0.1), color = self.bullet.get('color') or (250, 250, 0)))
        if self.bic:
            self.bullet_in_chamber -= 1
            if self.bullets > 0:
                self.bullets -= 1
                self.bullet_in_chamber = 1
        else:
            self.bullets -= 1

    def reload(self):
        step = self.reload_progress//self.time_per_reload_step
        if self.reload_progress >= self.reload_time:
            self.image, self.rect = self.extra_reload_sprite
        else:
            self.image, self.rect = self.reload_sprites[int(step)]
        self.reload_progress += 1
        if self.reload_progress >= self.reload_time + (self.bic-self.bullet_in_chamber)*self.reload_on_empty:
            if self.reload_type == 0:
                self.bullets = self.bullets_per_mag
                self.reloading = False
            if self.reload_type == 1:
                self.bullets += 1
                if self.bullets >= self.bullets_per_mag:
                    self.reloading = False
            if self.bic and self.bullet_in_chamber == 0:
                self.bullets -= 1
                self.bullet_in_chamber += 1
            self.reload_progress = 0
            self.mags -= 1

    def update(self, pX, pY, shoot: bool, reload: bool):
        self.image, self.rect = self.default
        self.rtn = shoot
        if shoot and self.reload_type == 1:
            self.reloading = False
            self.reload_progress = 0
        #Reloading
        if reload == True and self.bullets <= self.bullets_per_mag:
            self.reloading = True
        if self.reloading == True and self.mags > 0:
            if self.reload_type == 0:
                self.bullets = 0
            self.reload()
            self.rtn = False
        else: self.reloading = False
        #Shooting
        x = pX + self.weapon["shiftX"]
        y = pY + self.weapon["shiftY"]
        if self.clock < self.ticksToFire:
            self.clock+=1
        if shoot and self.clock >= self.ticksToFire:
            if self.bic:
                if self.bullet_in_chamber == 0:
                    if self.bullets > 0:
                        self.bullets -= 1
                        self.bullet_in_chamber = 1
                if self.bullet_in_chamber == 1:
                    self.clock -= self.ticksToFire
                    self.shoot(x, y)
            else:
                self.clock -= self.ticksToFire
                self.shoot(x, y)
            if self.weapon["burst"] == 1:
                self.rtn = False
        if self.fire_animation_time > 0:
            self.fire_animation_time -= 1
            self.image, self.rect = self.fire_sprite
        #Recoil
        self.update_recoil(shoot, self.recoil, self.recoil_control, self.max_recoil)
        #UI
        self.send_to_ui()
        #Drawing
        self.rect.topleft = (x, y)