import cv2
import numpy as np
import math

# path to the folder where the images will be saved
IM_PATH = "source_images/videoCapTest/"

# name of the video file
VIDEO_NAME = "source_images_video/v1.mp4"
# The frame capturing rate: the code captures 1 frame every CAP_RATE seconds
CAP_RATE = 0.5


cap = cv2.VideoCapture(VIDEO_NAME)
frameRate = cap.get(5)
multiplier = int(round(CAP_RATE * frameRate))
print(cap)
# name of the next image to be saved
im_index = 1

while(cap.isOpened()):

    # the ID of the current frame
    frameID = int(round(cap.get(1)))
    ret, frame = cap.read()

    # checks whether a frame was sucessfully captured
    if(ret == True):
        # this is so that we only capture 1 frame every 1 second
        # if(frameID % math.floor(frameRate) == 0):
        if(frameID % multiplier == 0):
            print(IM_PATH+str(im_index)+'.jpg')
            cv2.imwrite(IM_PATH+str(im_index)+'.jpg',frame)
            im_index+= 1
        else:
            break


cap.release()




