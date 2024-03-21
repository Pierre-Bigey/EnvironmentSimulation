import random
from abc import abstractmethod

import pygame

class Living(pygame.sprite.Sprite):


    def __init__(self, all_sprites, x, y, life_expectancy, reproductive_cooldown, mature_ratio, old_ratio):
        super().__init__(all_sprites)
        self.all_sprites = all_sprites
        self.x = x
        self.y = y

        self.age = 0
        self.reproductive_cooldown = reproductive_cooldown
        self.mature_ratio = mature_ratio
        self.old_ratio = old_ratio
        self.rounds_since_last_reproduction = 0

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
        pass


    @abstractmethod
    def reproduce(self):
        # Placeholder method for reproduction process
        pass

    @abstractmethod
    def get_nutrient(self):
        pass

    def die(self):
        self.kill()
        # print("living die")
        # Placeholder method for death process
        pass

class Living2():

    def __init__(self):


        pass
