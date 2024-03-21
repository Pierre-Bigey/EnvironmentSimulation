import math
import random
from abc import abstractmethod
from enum import Enum

from living import Living


class Animal(Living):

    class State(Enum):
        SEARCHING_FOR_FOOD = 1
        SEARCHING_FOR_PARTNER = 2

    initial_satiety = 1000
    min_satiety_to_breed = 400
    min_satiety_to_search_for_food = 100

    def __init__(self, x, y, life_expectancy, reproductive_cooldown, reproductive_age, reproductive_rate, given_speed):
        super().__init__(x, y, life_expectancy, reproductive_cooldown, reproductive_age, reproductive_rate)

        #print the creation of the animal with its parameters
        print("Animal created with x {}, y {}, life_expectancy {}, reproductive_cooldown {}, reproductive_age {}, reproductive_rate {}, given_speed {}".format(x, y, life_expectancy, reproductive_cooldown, reproductive_age, reproductive_rate, given_speed))

        self.speed = random.uniform(0.8, 1.1) * given_speed

        self.satiety = Animal.initial_satiety  # Initial satiety level (can be adjusted)

        self.state = Animal.State.SEARCHING_FOR_FOOD

        self.target = None

        self.partner_target = None


    def move(self, destination):
        # Calculate the distance to the destination
        dx = destination[0] - self.x
        dy = destination[1] - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        # Calculate the angle to the destination
        angle = math.atan2(dy, dx)

        # Calculate the movement along x and y axes using speed
        move_x = math.cos(angle) * self.speed
        move_y = math.sin(angle) * self.speed

        # Move the animal towards the destination
        self.x += move_x
        self.y += move_y

        # Update the position of the animal's sprite
        self.rect.center = (self.x, self.y)

    def eat(self, food):
        nutriment = food.get_nutrient()
        self.satiety += nutriment  # Example: Increase satiety by the nutriment value of the food
        food.die()  # Remove the food from the sprite group
        self.target = None
        pass


    def reproduce(self, partner):
        self.rounds_since_last_reproduction = 0

        pass


    def die(self):
        super().die()
        #Show nutriment and satiety when animal die
        print("animal die, satiety {}, age {}, die age {} ".format(self.satiety, self.age, self.die_age))
        # Implement death behavior
        pass

    def update(self):
        super().update()

        # Decrease satiety
        self.satiety -= 1  # Example: Decrease satiety by 1 unit per frame

        # Decide the state
        if self.satiety <= 0:
            # If satiety level is zero or below, the animal dies due to hunger
            self.die()

        elif self.satiety <= Animal.min_satiety_to_search_for_food:
            # If satiety level is below 50, the animal searches for food
            self.state = Animal.State.SEARCHING_FOR_FOOD

        elif self.age >= self.reproductive_age and self.rounds_since_last_reproduction >= self.reproductive_cooldown and self.satiety >= Animal.min_satiety_to_breed:
            # If the animal is old enough and ready to reproduce, it searches for a partner
            self.state = Animal.State.SEARCHING_FOR_PARTNER

        else:
            # Otherwise, the animal continues its regular behavior
            self.state = Animal.State.SEARCHING_FOR_FOOD

        if(self.state == Animal.State.SEARCHING_FOR_FOOD):
            self.search_for_food()
        elif(self.state == Animal.State.SEARCHING_FOR_PARTNER):
            self.search_for_partner()


    def search_for_food(self):
        # Implement searching for food behavior for animals
        pass

    def search_for_partner(self):
        # Implement searching for a partner behavior for animals
        pass