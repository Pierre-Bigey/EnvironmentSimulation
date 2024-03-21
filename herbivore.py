import math
import random

import pygame

from animal import Animal
from plant import Plant


class Herbivore(Animal):
    reproductive_rate = 30
    reproductive_age = 1000
    reproductive_cooldown = 500
    life_expectancy = 5000
    speed = 0.8

    def __init__(self, x, y, all_herbivores, all_plants):
        super().__init__(x, y, Herbivore.life_expectancy, Herbivore.reproductive_cooldown, Herbivore.reproductive_age,
                         Herbivore.reproductive_rate, Herbivore.speed)

        self.all_herbivores = all_herbivores
        self.all_plants = all_plants
        self.target : Plant = None

        # Set a rectangle of 15px
        self.image = pygame.Surface((15, 15))
        # Add more attributes as needed

        self.color = self.config_reader.get_herbivore_color()

    def update(self):
        super().update()
        self.image.fill(self.color)

    def search_for_food(self):
        if(self.target == None):
            self.target = self.find_nearest_plant()
        else:
            self.move((self.target.x, self.target.y))
            if self.rect.colliderect(self.target.rect):
                self.eat(self.target)
        pass

    def find_nearest_plant(self):
        # Calculate distances to all plants
        distances = [(plant, math.sqrt((plant.x - self.x) ** 2 + (plant.y - self.y) ** 2)) for plant in self.all_plants]

        # Sort the distances and return the closest plant
        if distances:
            closest_plant, _ = min(distances, key=lambda x: x[1])
            return closest_plant
        else:
            return None

    def search_for_partner(self):
        if(self.partner_target == None):
            self.partner_target = self.find_partner()
        else:
            self.move((self.partner_target.x, self.partner_target.y))
            if self.rect.colliderect(self.partner_target.rect):
                self.reproduce(self.partner_target)
                self.partner_target = None



    def find_partner(self):
        # Get a list of  all herbivors that are in search for partner
        possible_partners = [herbivore for herbivore in self.all_herbivores if herbivore != self and herbivore.state == Animal.State.SEARCHING_FOR_PARTNER]
        #calculate the distance to all possible partners
        distances = [(herbivore, math.sqrt((herbivore.x - self.x) ** 2 + (herbivore.y - self.y) ** 2)) for herbivore in possible_partners]
        # Sort the distances and return the closest partner
        if distances:
            closest_partner, _ = min(distances, key=lambda x: x[1])
            return closest_partner
        else:
            return None

    def reproduce(self, partner):
        super().reproduce(partner)

        distance = random.uniform(5, 15)

        # Generate random angle in radians
        angle = random.uniform(0, 2 * math.pi)

        # Calculate new_x and new_y using polar coordinates
        new_x = self.x + distance * math.cos(angle)
        new_y = self.y + distance * math.sin(angle)
        # Check if the living is not out of screen border, else abort the creation

        # Create a new instance of the plant with random position
        self.instantiate_herbivore(new_x, new_y, self.all_herbivores, self.all_plants)

    def get_nutrient(self):
        return self.satiety*1.2


    def die(self):
        super().die()
        # Remove the plant from the sprite group
        self.all_herbivores.remove(self)

        # Free up any resources associated with the plant
        del self

    @staticmethod
    def instantiate_herbivore(x, y, all_herbivores, all_plants):
        if (len(all_herbivores) > 200):
            return None
        herbivore = Herbivore(x, y, all_herbivores, all_plants)
        all_herbivores.add(herbivore)
        # QuadTreeService.get_instance().get_quadtree("plant").insert(plant)
        return herbivore

