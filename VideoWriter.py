import cv2
from cv2 import VideoWriter, VideoWriter_fourcc
import numpy as np
from Constants import *


class SimVideoWriter:

    def __init__(self, path='./simulation.avi', width=1920, height=1080, fps=10):
        self.width = width
        self.height = height
        self.video = VideoWriter(path, VideoWriter_fourcc(*'mp4v'),
                                 float(fps), (width, height))
        self.cellWidth = np.floor(width / worldWidth)
        self.cellHeight = np.floor(height / worldHeight)


    def end(self):
        self.video.release()


    def writeFrame(self, world):
        frame = np.empty((self.height, self.width, 3), dtype=np.uint8)
        frame[:,:] = backgroundColor

        for cell in world.cells:

            ageFactor = (cell.maxAge - cell.age) / cell.maxAge         # 1 -> young,   0 -> old
            lifePointsFactor = cell.lifePoints / cell.maxLifePoints    # 1 -> healthy, 0 -> damaged
            alpha = int(255.0 * (ageFactor + lifePointsFactor) / 2.0)
            color = tuple(reversed(colors[cell.team]))  # BGR

            pt1 = (int(cell.col * self.cellWidth), int(cell.row * self.cellHeight))
            pt2 = (int((cell.col + 1) * self.cellWidth), int((cell.row + 1) * self.cellHeight))

            rect = cv2.Mat()
            frame.copyTo(rect)
            cv2.rectangle(rect, pt1=pt1, pt2=pt2, color=color, thickness=-1)
            cv2.addWeighted(rect, alpha, frame, 1 - alpha, 0, frame)

            # white_rect = np.ones(sub_img.shape, dtype=np.uint8) * 255
            # res = cv2.addWeighted(sub_img, 0.5, white_rect, 0.5, 1.0)

        self.video.write(frame)