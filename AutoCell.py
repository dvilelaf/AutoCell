import pygame
import time
import sys
import numpy as np
from World import World, colors
from Cell import Cell
from Constants import *
from Log import Plot
from VideoWriter import SimVideoWriter

# Cell size
cellWidth = np.floor(windowWidth / worldWidth)
cellHeight = np.floor(windowHeight / worldHeight)

# Initialization
world = World(worldWidth, worldHeight, initialPopulation=startingPopulation, nTeams=nTeams)
pause = False

if showWindow:
    pygame.init()
    screen = pygame.display.set_mode((windowWidth, windowHeight))

plot = Plot(world) if showPlot else None
video = SimVideoWriter() if writeVideo else None

# Loop
while True:

    if not pause:
        world.step()

        # Screen update
        if showWindow:
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
                color = colors['blue'] if cell.infected == -1 else colors['yellow']
                if cell.passedIt:
                    color = colors['green']
                surface.fill(color)
                surface.set_alpha(255)
                screen.blit(surface, (cell.col * cellWidth, cell.row * cellHeight))

            pygame.display.flip()

        # Write video
        if writeVideo:
            video.writeFrame(world)

        # Plot
        if showPlot:
            plot.update(world)

        if world.epoch == 1:
            pause = True

        # Pause when no infected cells remain
        # if world.data['infected'] == 0:
        #     pause = True
            # if writeVideo:
            #     video.end()
            # pygame.quit()
            # sys.exit()

    if showWindow:
        # Keyboard event check
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if writeVideo:
                    video.end()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                pause = not pause

        # Sleep
        time.sleep(frameWait)