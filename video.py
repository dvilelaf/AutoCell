import cv2
import numpy as np
from cv2 import VideoWriter, VideoWriter_fourcc

width = 1920
height = 1080
FPS = 30
seconds = 2
radius = 150
paint_h = int(height/2)

video = VideoWriter('./circle_noise.avi', VideoWriter_fourcc(*'mp4v'), float(FPS), (width, height))

for _ in range(seconds*FPS):
    # frame = np.random.randint(0, 256,
    #                           (height, width, 3),
    #                           dtype=np.uint8)


    frame = np.empty((height, width, 3), dtype=np.uint8)
    frame[:,:] = (255, 255, 255)
    # frame.fill(30)

    # cv2.circle(frame, (paint_x, paint_h), radius, (0, 0, 0), -1)

    cv2.rectangle(frame, pt1=(200,200), pt2=(300,300), color=(50,50,50), thickness=-1)

    video.write(frame)

video.release()