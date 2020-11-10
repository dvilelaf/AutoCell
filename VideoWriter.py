import cv2
from cv2 import VideoWriter, VideoWriter_fourcc
import numpy as np
from Constants import *


class SimVideoWriter:

    def __init__(self, path='./simulation.mkv', width=videoWidth, height=videoHeight, fps=videoFPS):
        self.width = width
        self.height = height
        self.video = VideoWriter(path, VideoWriter_fourcc(*'avc1'), # *'HFYU' for lossless
                                 float(fps), (width, height))
        self.cellWidth = np.floor(width / worldWidth)
        self.cellHeight = np.floor(height / worldHeight)


    def end(self):
        self.video.release()


    def writeFrame(self, world):
        frame = np.empty((self.height, self.width, 3), dtype=np.uint8)
        frame[:,:] = backgroundColor

        for cell in world.cells:

            cellColor = tuple(reversed(colors[cell.team])) # BGR
            ageFactor = (cell.maxAge - cell.age) / cell.maxAge         # 1 -> young,   0 -> old
            lifePointsFactor = cell.lifePoints / cell.maxLifePoints    # 1 -> healthy, 0 -> damaged
            alpha = (ageFactor + lifePointsFactor) / 2.0

            pt1 = (int(cell.col * self.cellWidth), int(cell.row * self.cellHeight))
            pt2 = (int((cell.col + 1) * self.cellWidth), int((cell.row + 1) * self.cellHeight))

            cellBackground = frame[pt1[1] : pt2[1], pt1[0] : pt2[0]] # Beware, X and Y must be reversed here

            cellArea = np.ones(cellBackground.shape, dtype=np.uint8)
            for i in range(3):
                cellArea[:,:,i] = cellColor[i]

            blend = cv2.addWeighted(cellBackground, (1 - alpha), cellArea, alpha, 0)
            frame[pt1[1] : pt2[1], pt1[0] : pt2[0]] = blend

        self.video.write(frame)
