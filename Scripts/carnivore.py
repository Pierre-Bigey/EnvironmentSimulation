import math
import random

import pygame

from Scripts.animal import Animal
from Utils.configReader import ConfigReader
from Scripts.herbivore import Herbivore  # Import Herbivore class instead of Plant


class Carnivore(Animal):
    carnivore_config_reader = ConfigReader("Configs/carnivore_config.json")
    # retrieving the values from the config file
    reproductive_cooldown = carnivore_config_reader.get_config("reproductive_cooldown")
    mature_ratio = carnivore_config_reader.get_config("mature_ratio")
    old_ratio = carnivore_config_reader.get_config("old_ratio")
    life_expectancy = carnivore_config_reader.get_config("life_expectancy")
    min_nutriment = carnivore_config_reader.get_config("min_nutriment")
    max_nutriment = carnivore_config_reader.get_config("max_nutriment")
    speed = carnivore_config_reader.get_config("speed")
    initial_satiety = carnivore_config_reader.get_config("initial_satiety")
    min_satiety_to_search_for_food = carnivore_config_reader.get_config("min_satiety_to_search_for_food")
    min_satiety_to_breed = carnivore_config_reader.get_config("min_satiety_to_breed")
    min_reproduction_distance = carnivore_config_reader.get_config("min_reproduction_distance")
    max_reproduction_distance = carnivore_config_reader.get_config("max_reproduction_distance")

    def __init__(self, all_sprites, all_plants, all_herbivores, all_carnivores, x, y):
        super().__init__(all_sprites, all_plants, all_herbivores, all_carnivores, x, y, Carnivore.min_reproduction_distance,
                         Carnivore.max_reproduction_distance, Carnivore.life_expectancy, Carnivore.reproductive_cooldown,
                         Carnivore.mature_ratio, Carnivore.old_ratio, Carnivore.speed, Carnivore.initial_satiety,
                         Carnivore.min_satiety_to_search_for_food, Carnivore.min_satiety_to_breed)

        print("carnivore created")
        # Add more attributes as needed
        self.all_carnivores.add(self)

        self.classic_color = Carnivore.carnivore_config_reader.get_config("color")
        self.breeding_color = Carnivore.carnivore_config_reader.get_config("breeding_color")

    def collide(self, colliders):
        super().collide(colliders)
        # print("carnivore collided with: ", colliders)
        # Get herbivores from colliders
        herbivores = [collider for collider in colliders if isinstance(collider, Herbivore)]
        # Eat herbivores
        for herbivore in herbivores:
            self.eat(herbivore)

    def update(self):
        super().update()
        if self.can_breed():
            self.image.fill(self.breeding_color)
        else:
            self.image.fill(self.classic_color)

    def search_for_food(self):
        # print("searching for food with target group: ", self.target_group)
        if not self.target_group:
            self.target_group.add(self.find_nearest_herbivore())

    def find_nearest_herbivore(self):
        # Calculate distances to all herbivores
        distances = [(herbivore, math.sqrt((herbivore.x - self.x) ** 2 + (herbivore.y - self.y) ** 2)) for herbivore in
                     self.all_herbivores]

        # Sort the distances and return the closest herbivore
        if distances:
            closest_herbivore, _ = min(distances, key=lambda x: x[1])
            return closest_herbivore
        else:
            return None

    def search_for_partner(self):
        if not self.target_group or not isinstance(self.target_group.sprite, Carnivore):
            self.target_group.empty()
            partner = self.find_partner()
            if partner:
                self.target_group.add(partner)

    def find_partner(self):
        # Get a list of all carnivores that are in search for partner
        possible_partners = [carnivore for carnivore in self.all_carnivores if
                             carnivore != self and carnivore.can_breed() and len(carnivore.groups()) <= 2]
        # Calculate the distance to all possible partners
        distances = [(carnivore, math.sqrt((carnivore.x - self.x) ** 2 + (carnivore.y - self.y) ** 2)) for carnivore in
                     possible_partners]
        # Sort the distances and return the closest partner
        if distances:
            closest_partner, _ = min(distances, key=lambda x: x[1])
            return closest_partner
        else:
            return None

    def reproduce(self, partner):
        print("carnivore reproducing, id = ", id(self), " partner id = ", id(partner))

        new_x, new_y = super().reproduce(partner)
        # print("got new x and y: ", new_x, " ", new_y)

        if id(self) > id(partner):
            self.target_group.empty()
            return

        self.target_group.empty()

        print("carnivore can reproduce !!!")

        Carnivore(self.all_sprites, self.all_plants, self.all_herbivores, self.all_carnivores, new_x, new_y)

    def get_nutrient(self):
        return self.satiety * 1.2

    def die(self):
        super().die()
        del self
