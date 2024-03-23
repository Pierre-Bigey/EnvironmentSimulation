import math
import random

import pygame

from Utils.configReader import ConfigReader
from animal import *
from plant import Plant


class Herbivore(Animal):
    herbivore_config_reader = ConfigReader("Configs/herbivore_config.json")
    # retrieving the values from the config file
    reproductive_cooldown = herbivore_config_reader.get_config("reproductive_cooldown")
    mature_ratio = herbivore_config_reader.get_config("mature_ratio")
    old_ratio = herbivore_config_reader.get_config("old_ratio")
    life_expectancy = herbivore_config_reader.get_config("life_expectancy")
    min_nutriment = herbivore_config_reader.get_config("min_nutriment")
    max_nutriment = herbivore_config_reader.get_config("max_nutriment")
    speed = herbivore_config_reader.get_config("speed")
    initial_satiety = herbivore_config_reader.get_config("initial_satiety")
    min_satiety_to_search_for_food = herbivore_config_reader.get_config("min_satiety_to_search_for_food")
    min_satiety_to_breed = herbivore_config_reader.get_config("min_satiety_to_breed")
    min_reproduction_distance = herbivore_config_reader.get_config("min_reproduction_distance")
    max_reproduction_distance = herbivore_config_reader.get_config("max_reproduction_distance")

    def __init__(self, all_sprites, all_plants, all_herbivores, all_carnivores, x, y):
        super().__init__(all_sprites, all_plants, all_herbivores, all_carnivores, x, y, Herbivore.min_reproduction_distance,
                         Herbivore.max_reproduction_distance, Herbivore.life_expectancy, Herbivore.reproductive_cooldown,
                         Herbivore.mature_ratio, Herbivore.old_ratio, Herbivore.speed, Herbivore.initial_satiety,
                         Herbivore.min_satiety_to_search_for_food, Herbivore.min_satiety_to_breed)

        print("herbivore created")
        # Add more attributes as needed
        self.all_herbivores.add(self)

        self.classic_color = Herbivore.herbivore_config_reader.get_config("color")
        self.breeding_color = Herbivore.herbivore_config_reader.get_config("breeding_color")

    def collide(self, colliders):
        super().collide(colliders)
        # print("herbivore collided with: ", colliders)
        #Get plants from colliders
        plants = [collider for collider in colliders if isinstance(collider, Plant)]
        #Eat plants
        for plant in plants:
            self.eat(plant)

    def update(self):
        super().update()
        if(self.can_breed()):
            self.image.fill(self.breeding_color)
        else:
            self.image.fill(self.classic_color)

    def search_for_food(self):
        #print("searching for food with target group: ", self.target_group)
        if not(self.target_group):
            self.target_group.add(self.find_nearest_plant())

    def find_nearest_plant(self):
        # print("finding nearest plant with all_plants: ", self.all_plants)
        # Calculate distances to all plants
        distances = [(plant, math.sqrt((plant.x - self.x) ** 2 + (plant.y - self.y) ** 2)) for plant in self.all_plants if len(plant.groups()) <= 2]

        # Sort the distances and return the closest plant
        if distances:
            closest_plant, _ = min(distances, key=lambda x: x[1])
            return closest_plant
        else:
            return None

    def search_for_partner(self):
        if not self.target_group or not isinstance(self.target_group.sprite, Herbivore):
            self.target_group.empty()
            partner = self.find_partner()
            if partner:
                self.target_group.add(partner)

    def find_partner(self):
        # Get a list of  all herbivors that are in search for partner
        possible_partners = [herbivore for herbivore in self.all_herbivores if
                             herbivore != self and isinstance(herbivore.state, SearchingForPartnerState)]
        # calculate the distance to all possible partners
        distances = [(herbivore, math.sqrt((herbivore.x - self.x) ** 2 + (herbivore.y - self.y) ** 2)) for herbivore in
                     possible_partners]
        # Sort the distances and return the closest partner
        if distances:
            closest_partner, _ = min(distances, key=lambda x: x[1])
            return closest_partner
        else:
            return None

    def reproduce(self, partner):

        new_x, new_y = super().reproduce(partner)
        # print("got new x and y: ", new_x, " ", new_y)
        self.target_group.empty()
        if id(self) > id(partner):
            # self.target_group.empty()
            return



        #print("herbivore can reproduce !!!")

        Herbivore(self.all_sprites, self.all_plants, self.all_herbivores, self.all_carnivores, new_x, new_y)

    def get_nutrient(self):
        return self.satiety * 1.2

    def die(self):
        super().die()
        del self

