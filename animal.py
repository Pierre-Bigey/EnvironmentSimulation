import math
import random
from abc import abstractmethod
from enum import Enum

import pygame.sprite

from living import Living


class Animal(Living):

    # Class of the state searching for food

    def __init__(self, all_sprites, all_plants, all_herbivores, all_carnivores, x, y, min_reproduction_distance,
                 max_reproduction_distance, life_expectancy, reproductive_cooldown, mature_ratio, old_ratio, given_speed,
                 initial_satiety, min_satiety_to_search_for_food, min_satiety_to_breed, ):
        super().__init__( all_sprites, all_plants, all_herbivores, all_carnivores, x, y, life_expectancy,
                          reproductive_cooldown, mature_ratio, old_ratio, min_reproduction_distance, max_reproduction_distance)

        self.all_plants = all_plants
        self.all_herbivores = all_herbivores
        self.all_carnivores = all_carnivores

        self.min_reproduction_distance = min_reproduction_distance
        self.max_reproduction_distance = max_reproduction_distance

        self.speed = random.uniform(0.8, 1.1) * given_speed

        self.satiety = initial_satiety  # Initial satiety level (can be adjusted)
        self.min_satiety_to_search_for_food = min_satiety_to_search_for_food
        self.min_satiety_to_breed = min_satiety_to_breed

        self.state = SearchingForFoodState(self)

        self.target_group = pygame.sprite.GroupSingle()

        # Set a rectangle of 15px
        self.image = pygame.Surface((15, 15))


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

    def collide(self, colliders):
        # Check if some same class are present in the colliders
        #print("my class is : ", self.__class__)
        #print("colliding with : ", [collider.__class__ for collider in colliders])
        same_class = [collider for collider in colliders if isinstance(collider, self.__class__)]
        if same_class:
            # print("collided with same class : ", same_class)
            for same in same_class:
                #print("can breed : ", same.can_breed())
                if self.can_breed() and same.can_breed():
                    self.reproduce(same_class[0])
                    same_class[0].reproduce(self)



    def eat(self, food):
        nutriment = food.get_nutrient()
        self.satiety += nutriment  # Example: Increase satiety by the nutriment value of the food
        food.die()  # Remove the food from the sprite group
        pass

    def reproduce(self, partner):
        # print("animal reproduce")

        return super().reproduce()

    def update(self):
        super().update()

        # Decrease satiety
        self.satiety -= 1  # Example: Decrease satiety by 1 unit per frame

        # Decide the state
        if self.satiety <= 0:
            # If satiety level is zero or below, the animal dies due to hunger
            self.die()
            return

        self.state = self.state.process()

        if(self.target_group):
            self.move((self.target_group.sprite.x, self.target_group.sprite.y))

    def search_for_food(self):
        # Implement searching for food behavior for animals
        pass

    def search_for_partner(self):
        # Implement searching for a partner behavior for animals
        pass

    def can_breed(self):
        return (self.age >= self.mature_ratio*self.die_age and
                self.rounds_since_last_reproduction >= self.reproductive_cooldown and
                self.satiety >= self.min_satiety_to_breed)

    def do_need_to_search_for_food(self):
        return self.satiety <= self.min_satiety_to_search_for_food

    def die(self):
        super().die()
        pass


class State:
    class Event(Enum):
        START = 1
        UPDATE = 2
        EXIT = 3

    class STATE(Enum):
        SEARCHING_FOR_FOOD = 1
        SEARCHING_FOR_PARTNER = 2

    def __init__(self, state: STATE, animal: Animal):
        self.animal = animal
        self.stage = State.Event.START
        self.name = state
        self.next_state = None
        pass

    def start(self):
        self.stage = State.Event.UPDATE
        pass

    def update(self):
        self.stage = State.Event.UPDATE
        pass

    def exit(self):
        self.stage = State.Event.EXIT
        pass

    def process(self):
        if self.stage == State.Event.START:
            self.start()
        elif self.stage == State.Event.UPDATE:
            self.update()
        elif self.stage == State.Event.EXIT:
            self.exit()
            return self.next_state
        return self

class SearchingForFoodState(State):

    def __init__(self, animal: Animal):
        super().__init__(State.STATE.SEARCHING_FOR_FOOD, animal)
        pass

    def start(self):
        super().start()
        self.next_state = SearchingForPartnerState(self.animal)
        self.animal.search_for_food()

    def update(self):
        super().update()

        #Check if it should go search for bread
        if self.animal.can_breed():
            self.stage = State.Event.EXIT
            return

        #Check if target is still alive
        if not self.animal.target_group:
            self.stage = State.Event.START
            return


    def exit(self):
        super().exit()
        pass


class SearchingForPartnerState(State):

    def __init__(self, animal: Animal):
        super().__init__(State.STATE.SEARCHING_FOR_PARTNER, animal)

        pass

    def start(self):
        # print("GO Searching for partner !")
        super().start()
        self.next_state = SearchingForFoodState(self.animal)
        self.animal.search_for_partner()

    def update(self):
        super().update()

        #Check if it should go search for food
        if not self.animal.can_breed() or self.animal.do_need_to_search_for_food():
            self.stage = State.Event.EXIT
            return

        #Check if target is still alive
        if not self.animal.target_group:
            self.stage = State.Event.START
            return

        #Check if target still wants to breed
        if not self.animal.target_group.sprite.do_need_to_search_for_food:
            self.stage = State.Event.START
            return

    def exit(self):
        super().exit()

