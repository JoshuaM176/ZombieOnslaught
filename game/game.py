import math
import random as rand
from registries.zombie_registry import ZombieRegistry
from registries.bullet_registry import BulletRegistry
from entities.zombies import Zombie
from resources.resource_loader.resource_loader import ResourceLoader

class Game:

    def __init__(self):
        self.properties = {"wave": 0}
        self.spawn_rates = ["zombie"] * 500
        self.spawn_index = 0

    def new_wave(self, zombie_registry: ZombieRegistry, bullet_registry: BulletRegistry, x, y):
        self.properties["wave"] += 1
        wave = self.properties["wave"]
        number_of_zombies = math.floor(math.sqrt(wave*2))
        maxX = x + 100 + wave
        i = 0
        while i < number_of_zombies:
            zombie = self.spawn_rates[math.floor(rand.uniform(0,499.99))]
            zombie_registry.register(Zombie(zombie, rand.uniform(x, maxX), rand.uniform(0, y-506), bullet_registry, wave))
            i += 1

    def add_to_spawn_pool(self, zombie: str, num: int):
        i = 0
        while i < num:
            self.spawn_rates[self.spawn_index] = zombie
            self.spawn_index += 1
            if self.spawn_index >= 500:
                self.spawn_index = 0
            i+=1