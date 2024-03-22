import pygame


def grid_collision_detection(sprites: [pygame.sprite.Sprite], grid_size: int):
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
        for sprite1 in cell_rects:
            colliding_rects = []
            for other_cell_x in range(cell_key[0] - 1, cell_key[0] + 2):
                for other_cell_y in range(cell_key[1] - 1, cell_key[1] + 2):
                    if (other_cell_x, other_cell_y) in grid:
                        for sprite2 in grid[(other_cell_x, other_cell_y)]:
                            if sprite1 != sprite2 and sprite1.rect.colliderect(sprite2):
                                colliding_rects.append(sprite2)
            if colliding_rects:
                colliding_rects.append(sprite1)
                collisions.append(colliding_rects)

    return collisions
