import math
import random as rand
from registries.zombie_registry import ZombieRegistry
from registries.bullet_registry import BulletRegistry, TracerRegistry
from entities.player import Player
from entities.zombies import Zombie
from resources.resource_loader.resource_loader import ResourceLoader
import pygame as pg
from game.ui import UI
from entities.hitreg import hitreg, hitreg1

spawn_loader = ResourceLoader('spawn_rates', 'game')
spawn_loader.load_all()

class Game:

    def __init__(self, screen: pg.display):
        self.ui = UI(screen)
        self.screen = screen
        self.bullet_registry = BulletRegistry(TracerRegistry(1000, self.screen), 200)
        self.player = Player(self.screen, self.bullet_registry, pg.sprite.RenderPlain(()), self.ui)
        self.zombie_bullet_registry = BulletRegistry(TracerRegistry(1000, self.screen), 200)
        self.zombie_registry = ZombieRegistry(pg.sprite.RenderPlain(()), self.ui)
        self.properties = {"wave": 0, "experience": 0, "money": 0}
        self.spawn_rates = ["zombie"] * 500
        self.spawn_index = 0
        self.spawn_data = spawn_loader.get('spawn_rates')

    def new_wave(self, x, y):
        self.properties["wave"] += 1
        self.send_to_ui()
        for data in self.spawn_data:
            self.update_spawn_rates(data)
        wave = self.properties["wave"]
        number_of_zombies = math.floor(math.sqrt(wave*2))
        maxX = x + 100 + wave
        i = 0
        while i < number_of_zombies:
            zombie = self.spawn_rates[math.floor(rand.uniform(0,499.99))]
            self.zombie_registry.register(Zombie(zombie, rand.uniform(x, maxX), rand.uniform(0, y-506), self.zombie_bullet_registry, wave))
            i += 1

    def update_spawn_rates(self, data: dict):
        wave = self.properties["wave"]
        if wave >= data["start_round"] and wave <= data["end_round"]:
            rate = data["rate"]
            func = rate["function"]
            mult = rate["mult"]
            if func["name"] == "flat":
                for i in range(mult):
                    self.add_to_spawn_pool(data["zombie"])

    def add_to_spawn_pool(self, zombie):
        self.spawn_rates[self.spawn_index] = zombie
        self.spawn_index += 1
        if self.spawn_index == 500:
            self.spawn_index = 0

    def send_to_ui(self):
        info = self.properties
        self.ui.send({"game": info})

    def player_input(self, input):
        self.input = input

    def update(self):
        self.zombie_registry.end_of_frame()
        self.player.process(self.input)
        self.zombie_bullet_registry.update()
        self.bullet_registry.update()
        self.zombie_registry.update(self.screen)
        self.properties["money"]+=self.zombie_registry.get_money()
        if self.zombie_registry.isEmpty():
            self.new_wave(*self.screen.get_size())
        hitreg(self.zombie_registry, self.bullet_registry)
        hitreg1([self.player], self.zombie_bullet_registry.get())
        self.ui.draw()