import pygame
import os
from os.path import join

TILE_SIZE = 16
NUM_TILES_PER_ROW = 40
# Set the size of the display surface
DISPLAY_WIDTH = TILE_SIZE * NUM_TILES_PER_ROW
DISPLAY_HEIGHT = TILE_SIZE * NUM_TILES_PER_ROW

# Load the tileset image
tileset_image = pygame.image.load("img/Group_tiles/tiles1.png")

# Create a list to store the selected tile indices
selected_tile_indices = []

# Initialize Pygame
pygame.init()

# Create the display surface
display_surface = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))

# Create a buffer surface with the same size as the display surface
buffer_surface = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))

# Create a clock object to control the frame rate
clock = pygame.time.Clock()

# Set the initial scroll position
scroll_y = 0

# Run the game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get the index of the tile that was clicked on
            x, y = event.pos
            tile_x = x // TILE_SIZE
            tile_y = (y + scroll_y) // TILE_SIZE
            tile_index = tile_y * NUM_TILES_PER_ROW + tile_x
            # Add the index to the selected tiles list
            selected_tile_indices.append(tile_index)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                # Export the selected tiles
                for i, index in enumerate(selected_tile_indices):
                    tile_x = (index % NUM_TILES_PER_ROW) * TILE_SIZE
                    tile_y = (index // NUM_TILES_PER_ROW) * TILE_SIZE
                    tile_surface = tileset_image.subsurface(pygame.Rect(tile_x, tile_y, TILE_SIZE, TILE_SIZE))
                    filename = f"water_{i}.png"
                    pygame.image.save(tile_surface, filename)
                    print(f"Saved tile {i} to {os.path.abspath(filename)}")
            elif event.key == pygame.K_UP:
                # Scroll up
                scroll_y -= TILE_SIZE
            elif event.key == pygame.K_DOWN:
                # Scroll down
                scroll_y += TILE_SIZE

    # Draw the tileset image onto the buffer surface
    buffer_surface.blit(tileset_image, (0, 0))

    # Draw the borders around the selected tiles onto the buffer surface
    for index in selected_tile_indices:
        tile_x = (index % NUM_TILES_PER_ROW) * TILE_SIZE
        tile_y = (index // NUM_TILES_PER_ROW) * TILE_SIZE
        pygame.draw.rect(buffer_surface, (0, 255, 0), (tile_x, tile_y - scroll_y, TILE_SIZE, TILE_SIZE), 1)

    # Calculate the portion of the buffer surface to blit to the display surface, based on the scroll position
    buffer_rect = pygame.Rect(0, scroll_y, DISPLAY_WIDTH, DISPLAY_HEIGHT)
    display_rect = buffer_rect.clip(pygame.Rect(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT))
    display_surface.blit(buffer_surface, (0, 0), display_rect)

    # Update the display
    pygame.display.update()

    # Control the frame rate
    clock.tick(60)

