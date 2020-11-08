import pygame
import time
import sys
import numpy as np
from World import World, colors
from Cell import Cell
from Constants import *
from Log import Plot

# Cell size
cellWidth = np.floor(windowWidth / worldWidth)
cellHeight = np.floor(windowHeight / worldHeight)

# Initialization
pygame.init()
screen = pygame.display.set_mode((windowWidth, windowHeight))
world = World(worldWidth, worldHeight, population=startingPopulation, nTeams=nTeams)
pause = False
plot = Plot(world) if showPlot else None

# Loop
while True:

    # Screen update
    if not pause:
        world.step()

        screen.fill(backgroundColor)

        # Grid
        if gridOn:
            for i in range(worldWidth):
                pygame.draw.line(screen, gridColor, (i * cellWidth, 0), (i * cellWidth, windowHeight), width=1)
            for j in range(worldHeight):
                pygame.draw.line(screen, gridColor, (0, j * cellHeight), (windowWidth, j * cellHeight), width=1)

        # Cells
        for cell in world.cells:
            surface = pygame.Surface((cellWidth, cellHeight))
            surface.fill(colors[cell.team])

            ageFactor = (cell.maxAge - cell.age) / cell.maxAge         # 1 -> young,   0 -> old
            lifePointsFactor = cell.lifePoints / cell.maxLifePoints    # 1 -> healthy, 0 -> damaged
            surface.set_alpha(int(255.0 * (ageFactor + lifePointsFactor) / 2.0))

            screen.blit(surface, (cell.col * cellWidth, cell.row * cellHeight))

        pygame.display.flip()

        # Plot
        if showPlot:
            plot.update(world)

        # Exit when no alive cells remain
        if len(world.cells) == 0:
            pygame.quit()
            sys.exit()

    # Keyboard event check
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            pause = not pause

    # Sleep
    time.sleep(frameWait)