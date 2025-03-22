import pygame as pg
from resources.resource_loader.resource_loader import ResourceLoader
from entities.bullets import Bullet
from registries.bullet_registry import BulletRegistry
from resources.resources import load_sprite
from game.ui import UI
import random as rand

weapon_loader = ResourceLoader('weapons')
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
        self.init_recoil(**resources["weapon"]["recoil"])
        self.init_ammo(**resources["weapon"]["ammo"])
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

    def init_sprites(self, default, reloading, colorkey):
        self.default = load_sprite(default, 'weapons', colorkey)
        self.reload_sprites = []
        for sprite in reloading:
            self.reload_sprites.append(load_sprite(sprite, 'weapons', colorkey))
        self.time_per_reload_step = self.reload_time/len(self.reload_sprites)

    def init_recoil(self, recoil, recoil_control, max_recoil):
        self.recoil = recoil
        self.recoil_control = recoil_control
        self.max_recoil = max_recoil

    def init_ammo(self, bullets_per_mag, max_mags, reload_time):
        self.bullets = bullets_per_mag
        self.bullets_per_mag = bullets_per_mag
        self.mags = max_mags
        self.max_mags = max_mags
        self.reload_time = reload_time * 60
        self.reload_progress = 0
        self.reloading = False

    def send_to_ui(self):
        info = {"bullets": self.bullets, "max_bullets": self.bullets_per_mag, "mags": self.mags, "max_mags": self.max_mags, "reload_progress": self.reload_progress/self.reload_time, "reload_time_left": self.reload_time-self.reload_progress, "name": self.name}
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
        self.bullet["x"] = x + self.bullet["shiftX"]
        self.bullet["y"] = y + self.bullet["shiftY"]
        self.bullet_registry.register(Bullet(**self.bullet, hor = 20, ver = -self.ver + rand.normalvariate(0, 0.1), color = self.bullet.get('color') or (250, 250, 0)))
        self.bullets -= 1

    def reload(self):
        step = self.reload_progress//self.time_per_reload_step
        self.image, self.rect = self.reload_sprites[int(step)]
        self.reload_progress += 1
        #self.image, self.rect = self.reload_sprites[step]
        if self.reload_progress >= self.reload_time:
            self.bullets = self.bullets_per_mag
            self.reload_progress = 0
            self.reloading = False
            self.image, self.rect = self.default

    def update(self, pX, pY, shoot: bool, reload: bool):
        self.rtn = shoot
        #Reloading
        if reload == True:
            self.reloading = True
        if self.reloading == True:
            self.reload()
            self.rtn = False
        #Shooting
        x = pX + self.weapon["shiftX"]
        y = pY + self.weapon["shiftY"]
        if self.clock < self.ticksToFire:
            self.clock+=1
        if shoot and self.clock >= self.ticksToFire and self.bullets > 0 and self.reloading == False:
            self.clock -= self.ticksToFire
            self.shoot(x, y)
            if self.weapon["burst"] == 1:
                self.rtn = False
        #Recoil
        self.update_recoil(shoot, self.recoil, self.recoil_control, self.max_recoil)
        #UI
        self.send_to_ui()
        #Drawing
        self.rect.topleft = (x, y)