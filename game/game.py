import math
import random as rand
from registries.zombie_registry import ZombieRegistry
from registries.bullet_registry import BulletRegistry
from entities.zombies import Zombie
from resources.resource_loader.resource_loader import ResourceLoader
from pathlib import Path
from game.ui import UI

spawn_loader = ResourceLoader('spawn_rates', 'game')
spawn_loader.load_all()

class Game:

    def __init__(self, ui: UI):
        self.ui = ui
        self.properties = {"wave": 0}
        self.spawn_rates = ["zombie"] * 500
        self.spawn_index = 0
        self.spawn_data = spawn_loader.get('spawn_rates')

    def new_wave(self, zombie_registry: ZombieRegistry, bullet_registry: BulletRegistry, x, y):
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
            zombie_registry.register(Zombie(zombie, rand.uniform(x, maxX), rand.uniform(0, y-506), bullet_registry, wave))
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
                    print(i)

    def add_to_spawn_pool(self, zombie):
        self.spawn_rates[self.spawn_index] = zombie
        self.spawn_index += 1
        if self.spawn_index == 500:
            self.spawn_index = 0

    def send_to_ui(self):
        info = {"wave": self.properties["wave"]}
        self.ui.send({"game": info})
