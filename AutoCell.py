import pygame
import time
import sys
import numpy as np
from World import World, colors
from Cell import Cell

# Window pixel size
windowWwidth, windowHeight = 800, 800
# Number of cells
widthNcells, heightNcells = 100, 100
# Background color
backgroundColor = (25, 25, 25)
gridColor = (100, 100, 100)
cellColor = (255, 255, 255)

# Cell size
cellWidth = np.floor(windowWwidth / widthNcells)
cellHeight = np.floor(windowHeight / heightNcells)

# Initialization
pygame.init()
screen = pygame.display.set_mode((windowWwidth, windowHeight))
world = World(widthNcells, heightNcells, nTeams=3)
pause = False

# Loop
while True:

    # Screen update
    if not pause:
        world.step()

        screen.fill(backgroundColor)

        # for i in range(widthNcells):
        #     pygame.draw.line(screen, gridColor, (i * cellWidth, 0), (i * cellWidth, windowHeight), width=1)
        # for j in range(heightNcells):
        #     pygame.draw.line(screen, gridColor, (0, j * cellHeight), (windowWwidth, j * cellHeight), width=1)


        for cell in world.cells:

            surface = pygame.Surface((cellWidth, cellHeight))
            surface.fill(colors[cell.team])

            ageFactor = (cell.maxAge - cell.age) / cell.maxAge         # 1 -> young,   0 -> old
            lifePointsFactor = cell.lifePoints / cell.maxLifePoints    # 1 -> healthy, 0 -> damaged
            surface.set_alpha(int(255.0 * (ageFactor + lifePointsFactor) / 2.0))

            screen.blit(surface, (cell.col * cellWidth, cell.row * cellHeight))

            # pygame.draw.polygon(screen, colors[cell.team],
            #                     ((cell.col      * cellWidth, cell.row       * cellHeight),
            #                     ((cell.col + 1) * cellWidth, cell.row       * cellHeight),
            #                     ((cell.col + 1) * cellWidth, (cell.row + 1) * cellHeight),
            #                      (cell.col      * cellWidth, (cell.row + 1) * cellHeight)),
            #                     width=0)

            # pygame.draw.circle(screen, colors[cell.team],
            #                    (cell.col * cellWidth + cellWidth/2, cell.row * cellHeight + cellWidth/2),
            #                    radius=cellWidth/2)

        pygame.display.flip()

    # Event check
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            pause = not pause
        # if sum(pygame.mouse.get_pressed()) > 0:
        #     posX, posY = pygame.mouse.get_pos()
        #     cellX, cellY = int(np.floor(posX / cellWidth)), int(np.floor(posY / cellHeight))

    # Sleep
    time.sleep(0.1)