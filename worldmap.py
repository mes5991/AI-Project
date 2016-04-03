import pygame
import numpy as np
from environment import Environment
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

pygame.init()

# Set the width and height of the screen [width, height]
M = 500
size = (M, M)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("World Map")
done = False
k = 1

# set the scaling factor based on screen size
z = M/100

# Used to manage how fast the screen updates
clock = pygame.time.Clock()
screen.fill(BLACK)
E1 = Environment((100, 100), .20, 4)

# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True# Flag that we are done so we exit this loop
    while k == 1:
        # Drawing code
        for i in range(100):
            for j in range(100):
                if E1.envMatrix[i,j] == 1.0:
                    m = i * z
                    n = j * z
                    pygame.draw.rect(screen, BLACK, [m, n, z, z])
                elif E1.envMatrix[i,j] == 2.0:
                    m = i * z
                    n = j * z
                    pygame.draw.rect(screen, RED, [m, n, z, z])
                else:
                    m = i * z
                    n = j * z
                    pygame.draw.rect(screen, WHITE, [m, n, z, z])
        k = 0
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
pygame.quit()