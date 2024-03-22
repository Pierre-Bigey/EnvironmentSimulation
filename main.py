import pygame
import random

from Utils import GridCollisionDetection
# from carnivore import Carnivore
from Utils.configReader import ConfigReader
# from herbivore import Herbivore
from plant import Plant

import matplotlib.pyplot as plt  # Import Matplotlib
import numpy as np  # Import NumPy

config_reader = ConfigReader("Configs/config.json")

# Set up the screen dimensions from the config file
SCREEN_WIDTH = config_reader.get_config("screen_width")
SCREEN_HEIGHT = config_reader.get_config("screen_height")

# Define colors from the config file
BACKGROUND_COLOR = config_reader.get_config("background_color")

# Simulation variables in numpy array
fps_data = np.array([0])  # Store FPS data
plant_count_data = np.array([0])  # Store plant count data


# herbivore_count_data = np.array([0])  # Store herbivore count data
# carnivore_count_data = np.array([0])  # Store herbivore count data


# Main function
def main():
    global plant_count_data, fps_data  # , herbivore_count_data, carnivore_count_data

    pygame.init()

    clock = pygame.time.Clock()

    def start():
        global all_sprites, all_plants
        all_sprites = pygame.sprite.Group()
        all_plants = pygame.sprite.Group()
        # all_herbivores = pygame.sprite.Group()
        # all_carnivores = pygame.sprite.Group()

        # Spawn initial plants
        for _ in range(10):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            Plant.instantiate_plant(all_sprites, x, y, all_plants)

        # Spawn initial herbivores
        # for _ in range(10):
        #     x = random.randint(0, SCREEN_WIDTH)
        #     y = random.randint(0, SCREEN_HEIGHT)
        #     Herbivore.instantiate_herbivore(x, y, all_herbivores, all_plants)
        #
        # #Spawn initial carnivores
        # for _ in range(4):
        #     x = random.randint(0, SCREEN_WIDTH)
        #     y = random.randint(0, SCREEN_HEIGHT)
        #     Carnivore.instantiate_carnivore(x, y, all_carnivores, all_herbivores)

    def physics():
        # Collision detection
        collisions = GridCollisionDetection.grid_collision_detection(all_plants,
                                                                     config_reader.get_config("collision_grid_size"))
        for collision in collisions:
            sprite = collision[0]
            # Remove sprite from the collision list
            collision.remove(sprite)
            sprite.collide(collision)

    def update():
        # update each plant
        all_sprites.update()

    def graphics():
        # Clear the screen
        screen.fill(BACKGROUND_COLOR)

        # Draw plants on the screen
        all_sprites.draw(screen)

        print_text()

        # update the display
        pygame.display.flip()

    def print_text():
        global plant_count_data, fps_data  # , herbivore_count_data, carnivore_count_data
        # Store data for plotting
        fps_data = np.append(fps_data, clock.get_fps())
        plant_count_data = np.append(plant_count_data, len(all_plants))
        # herbivore_count_data = np.append(herbivore_count_data, len(all_herbivores))
        # carnivore_count_data = np.append(carnivore_count_data, len(all_carnivores))

        # Render text (FPS, round_number, plant count, herbivore count and carnivores count)
        text_fps = font.render(f"FPS: {int(clock.get_fps())}", True, (0, 0, 0))  # Render FPS text
        text_frame = font.render(f"Frame: {int(len(fps_data))}", True, (0, 0, 0))  # Render frame text
        text_plant_count = font.render(f"Plant Count: {len(all_plants)}", True,
                                       (0, 0, 0))  # Render plant count text
        # text_herbivore_count = font.render(f"Herbivore Count: {len(all_herbivores)}", True, (0, 0, 0))
        # text_carnivore_count = font.render(f"Carnivore Count: {len(all_carnivores)}", True, (0, 0, 0))

        # Blit text onto the screen
        screen.blit(text_fps, (10, 10))  # Position of FPS text
        screen.blit(text_frame, (150, 10))
        screen.blit(text_plant_count, (10, 50))  # Position of plant count text
        # screen.blit(text_herbivore_count, (10, 90))
        # screen.blit(text_carnivore_count, (10, 130))

    # Font initialization
    font = pygame.font.Font(None, 36)  # You can replace "None" with a font file path if you want to load a custom font

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Environment Simulation")

    start()

    # Main loop
    running = True
    while running:
        # print(len(all_plants))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        physics()

        update()

        graphics()

        clock.tick(1000)

    pygame.quit()

    # Plot the data
    plt.plot(fps_data, label="FPS")
    plt.plot(plant_count_data, label="Plant Count")
    # plt.plot(herbivore_count_data, label="Herbivore Count")
    # plt.plot(carnivore_count_data, label="Carnivore Count")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
