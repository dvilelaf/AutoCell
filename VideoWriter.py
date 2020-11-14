import cv2
from cv2 import VideoWriter, VideoWriter_fourcc
import numpy as np
from Constants import *
import os.path


class SimVideoWriter:

    def __init__(self, path=videoPath, width=videoWidth, height=videoHeight, fps=videoFPS):

        if os.path.isfile(path):
            filename, extension = os.path.splitext(path)
            i = 0
            while os.path.isfile(path):
                path = filename + str(i) + extension
                i += 1

        self.width = width
        self.height = height
        codec = 'HFYU' if lossless else 'avc1'
        self.video = VideoWriter(path, VideoWriter_fourcc(*codec),
                                 float(fps), (width, height))
        self.cellWidth = np.floor(width / worldWidth)
        self.cellHeight = np.floor(height / worldHeight)


    def end(self):
        self.video.release()


    def writeFrame(self, world):
        frame = np.empty((self.height, self.width, 3), dtype=np.uint8)
        frame[:,:] = backgroundColor

        for cell in world.cells:

            color = colors['blue'] if cell.infected == -1 else colors['yellow']
            if cell.passedIt:
                color = colors['green']

            cellColor = tuple(reversed(color)) # BGR
            alpha = 1

            pt1 = (int(cell.col * self.cellWidth), int(cell.row * self.cellHeight))
            pt2 = (int((cell.col + 1) * self.cellWidth), int((cell.row + 1) * self.cellHeight))

            cellBackground = frame[pt1[1] : pt2[1], pt1[0] : pt2[0]] # Beware, X and Y must be reversed here

            cellArea = np.ones(cellBackground.shape, dtype=np.uint8)
            for i in range(3):
                cellArea[:,:,i] = cellColor[i]

            blend = cv2.addWeighted(cellBackground, (1 - alpha), cellArea, alpha, 0)
            frame[pt1[1] : pt2[1], pt1[0] : pt2[0]] = blend

        self.video.write(frame)
