import math
import random
import pygame

from Utils.configReader import ConfigReader
from living import Living


class Plant(Living):
    # Define class-level variables (fixed parameters)
    plant_config_reader = ConfigReader("Configs/plant_config.json")


    # Represents the minimum and maximum distance a new plant can be from the parent plant
    min_reproduction_distance = plant_config_reader.get_config("min_reproduction_distance")
    max_reproduction_distance = plant_config_reader.get_config("max_reproduction_distance")

    # Represents the number of rounds between each reproduction
    reproductive_cooldown = plant_config_reader.get_config("reproductive_cooldown")
    # Represents the age at which the plant is mature
    mature_ratio = plant_config_reader.get_config("mature_ratio")
    old_ratio = plant_config_reader.get_config("old_ratio")

    # Represents the minimum and maximum nutriment count of the plant
    min_nutriment = plant_config_reader.get_config("min_nutriment")
    max_nutriment = plant_config_reader.get_config("max_nutriment")

    # Represents the life expectancy of the plant
    life_expectancy = plant_config_reader.get_config("life_expectancy")

    nutriment_multiplier = plant_config_reader.get_config("nutriment_multiplier")

    max_plant = plant_config_reader.get_config("max_plant")

    def __init__(self, all_sprites, all_plants, all_herbivores, all_carnivores, x, y):
        if(len(all_plants) > Plant.max_plant):
            return
        super().__init__(all_sprites, all_plants, all_herbivores, all_carnivores, x, y, Plant.life_expectancy, Plant.reproductive_cooldown, Plant.mature_ratio,
                         Plant.old_ratio, Plant.min_reproduction_distance, Plant.max_reproduction_distance)

        all_plants.add(self)

        # Get the color of the plant from the config file
        self.color = self.plant_config_reader.get_config("color")

        self.nutriment_count = Plant.min_nutriment
        self.max_nutriment = Plant.max_nutriment * random.uniform(0.8, 1.2)

    def update(self):
        super().update()
        self.grow()
        self.update_nutriment_count()

        # Check if the plant has reached its die age
        # if self.is_covered_by_50_percent():
        #     self.die()

        # If the living is older enough, it can reproduce so it check with random and reproductive rate
        if self.age >= self.mature_ratio * self.die_age and self.rounds_since_last_reproduction >= self.reproductive_cooldown:
            self.reproduce()

    def grow(self):
        new_size = int(self.nutriment_count * 1.5)  # Example: increase size by 10 pixels for each unit of nutrient count
        self.image = pygame.transform.scale(self.image, (new_size, new_size))
        self.rect = self.image.get_rect(center=self.rect.center)
        self.image.fill(self.color)

    def collide(self, colliders):
        super().collide(colliders)

        # Check if the plant has been covered by 50% by other plants
        plants_colliders = [plant for plant in colliders if isinstance(plant, Plant)]
        self.is_covered_by_50_percent(plants_colliders)

    def update_nutriment_count(self):
        # Bell function for nutrient count based on age
        if self.age < self.die_age * Plant.mature_ratio:
            self.nutriment_count = self.age * self.max_nutriment / (self.die_age * Plant.mature_ratio)
        elif self.age > self.die_age * Plant.old_ratio:
            self.nutriment_count = self.max_nutriment * (self.age / self.die_age - 1) / (Plant.old_ratio - 1)
        else:  # It will decresase until reaching zero
            self.nutriment_count = self.max_nutriment
        self.nutriment_count = max(Plant.min_nutriment, self.nutriment_count)

    def reproduce(self):
        new_x, new_y = super().reproduce()

        # Check if the living is not out of screen border, else abort the creation
        if new_x < 0 or new_x > Living.global_config_reader.get_config(
                "screen_width") or new_y < 0 or new_y > Living.global_config_reader.get_config("screen_height"):
            return

        # Create a new instance of the plant with random position
        Plant(self.all_sprites, self.all_plants, self.all_herbivores, self.all_carnivores, new_x, new_y)

    def is_covered_by_50_percent(self, collision_group):

        # Calculate the total area covered by other rectangles in the collision group
        cliped_sprites = [sprite.rect.clip(self) for sprite in collision_group]
        covered_area = sum(cliped_rect.width * cliped_rect.height for cliped_rect in cliped_sprites)
        total_area = self.rect.width * self.rect.height

        # Calculate coverage percentage
        coverage_percentage = (covered_area / total_area) * 100

        # Return True if coverage is >= 50%
        if (coverage_percentage >= 50):
            self.die()

    def get_nutrient(self):
        return self.nutriment_count * Plant.nutriment_multiplier

    def die(self):
        super().die()
        # Free up any resources associated with the plant
        del self
