import math
import random

import pygame

from animal import Animal
from herbivore import Herbivore


class Carnivore(Animal):
    reproductive_rate = 30
    reproductive_age = 1200
    reproductive_cooldown = 1000
    life_expectancy = 4000
    speed = 0.65

    def __init__(self, x, y, all_carnivores, all_herbivores):
        super().__init__(x, y, Carnivore.life_expectancy, Carnivore.reproductive_cooldown, Carnivore.reproductive_age,
                         Carnivore.reproductive_rate, Carnivore.speed)

        self.all_carnivores = all_carnivores
        self.all_herbivores = all_herbivores
        self.target : Herbivore = None

        # Set a rectangle of 15px
        self.image = pygame.Surface((15, 15))
        # Add more attributes as needed

        self.color = self.config_reader.get_carnivore_color()

    def update(self):
        super().update()
        self.image.fill(self.color)

    def search_for_food(self):
        if(self.target == None):
            self.target = self.find_nearest_herbivor()
        else:
            self.move((self.target.x, self.target.y))
            if self.rect.colliderect(self.target.rect):
                self.eat(self.target)
        pass

    def find_nearest_herbivor(self):
        # Calculate distances to all herbivores
        distances = [(plant, math.sqrt((plant.x - self.x) ** 2 + (plant.y - self.y) ** 2)) for plant in self.all_herbivores]

        # Sort the distances and return the closest plant
        if distances:
            closest_herbivore, _ = min(distances, key=lambda x: x[1])
            return closest_herbivore
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
        possible_partners = [carnivore for carnivore in self.all_carnivores if carnivore != self and carnivore.state == Animal.State.SEARCHING_FOR_PARTNER]
        #calculate the distance to all possible partners
        distances = [(Carnivore, math.sqrt((Carnivore.x - self.x) ** 2 + (Carnivore.y - self.y) ** 2)) for Carnivore in possible_partners]
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
        self.instantiate_carnivore(new_x, new_y, self.all_carnivores, self.all_herbivores)


    def die(self):
        super().die()
        # Remove the plant from the sprite group
        self.all_carnivores.remove(self)

        # Free up any resources associated with the plant
        del self

    @staticmethod
    def instantiate_carnivore(x, y, all_carnivores, all_herbivores):
        if (len(all_carnivores) > 200):
            return None
        carnivore = Carnivore(x, y, all_carnivores, all_herbivores)
        all_carnivores.add(carnivore)
        # QuadTreeService.get_instance().get_quadtree("plant").insert(plant)
        return carnivore

