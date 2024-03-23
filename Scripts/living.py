import math
import random
from abc import abstractmethod

import pygame

from Utils.configReader import ConfigReader


class Living(pygame.sprite.Sprite):

    global_config_reader = ConfigReader("Configs/config.json")

    def __init__(self, all_sprites, all_plants, all_herbivores, all_carnivores, x, y, life_expectancy,
                 reproductive_cooldown, mature_ratio, old_ratio,
                 min_reproduction_distance, max_reproduction_distance):
        super().__init__(all_sprites)

        self.all_sprites = all_sprites
        self.all_plants = all_plants
        self.all_herbivores = all_herbivores
        self.all_carnivores = all_carnivores

        self.x = x
        self.y = y

        self.age = 0
        self.reproductive_cooldown = reproductive_cooldown
        self.mature_ratio = mature_ratio
        self.old_ratio = old_ratio
        self.rounds_since_last_reproduction = 0

        self.min_reproduction_distance = min_reproduction_distance
        self.max_reproduction_distance = max_reproduction_distance

        self.die_age = random.uniform(0.8, 1.1) * life_expectancy  # Random die age around 80-110% of life expectancy

        self.image = pygame.Surface((1, 1))  # Placeholder image for plant
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        # Placeholder method for the growth process
        self.age += 1

        self.rounds_since_last_reproduction += 1

        # Check if the plant has reached its die age
        if self.age >= self.die_age:
            self.die()

    def collide(self, colliders):
        # Placeholder method for collision process
        pass

    @abstractmethod
    def reproduce(self):
        self.rounds_since_last_reproduction = 0

        distance = random.uniform(self.min_reproduction_distance, self.max_reproduction_distance)

        # Generate random angle in radians
        angle = random.uniform(0, 2 * math.pi)

        # Calculate new_x and new_y using polar coordinates
        new_x = self.x + distance * math.cos(angle)
        new_y = self.y + distance * math.sin(angle)

        return new_x, new_y

    @abstractmethod
    def get_nutrient(self):
        pass

    @abstractmethod
    def get_nutrient(self):
        pass

    def die(self):
        self.kill()
        # print("living die")
        # Placeholder method for death process
        pass
