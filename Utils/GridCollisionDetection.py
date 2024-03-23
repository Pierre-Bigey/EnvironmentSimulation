import pygame

from Utils.configReader import ConfigReader

show_grid = ConfigReader("Configs/config.json").get_config("show_grid")

def grid_collision_detection(sprites: [pygame.sprite.Sprite], grid_size: int, screen):

    call_to_collide_rect = 0
    # Create a dictionary to store rectangles in each grid cell
    grid = {}
    for sprite in sprites:
        (x,y) = sprite.rect.center
        grid_key = (x // grid_size, y // grid_size)
        if grid_key in grid:
            grid[grid_key].append(sprite)
        else:
            grid[grid_key] = [sprite]

    # Check collisions in each grid cell and adjacent cells
    collisions = []
    for cell_key, cell_rects in grid.items():
        if (show_grid):
            x, y = cell_key
            rect = pygame.Rect(x*grid_size, y*grid_size, grid_size, grid_size)
            pygame.draw.rect(screen, (255, 255, 0), rect, 1)

        for sprite1 in cell_rects:
            colliding_rects = [sprite1]
            for other_cell_x in range(cell_key[0] - 1, cell_key[0] + 2):
                for other_cell_y in range(cell_key[1] - 1, cell_key[1] + 2):
                    if (other_cell_x, other_cell_y) in grid:
                        for sprite2 in grid[(other_cell_x, other_cell_y)]:
                            if sprite1 != sprite2:
                                call_to_collide_rect += 1
                                if sprite1.rect.colliderect(sprite2):
                                    colliding_rects.append(sprite2)

                    elif show_grid:
                        rect = pygame.Rect(other_cell_x * grid_size, other_cell_y * grid_size, grid_size, grid_size)
                        pygame.draw.rect(screen, (255, 0, 200), rect, 1)

            if len(colliding_rects) > 1:
                # colliding_rects.append(sprite1)
                collisions.append(colliding_rects)
    # print("call to collide rect : ", call_to_collide_rect)
    return collisions, call_to_collide_rect
