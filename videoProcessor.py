import cv2
import numpy as np
import math

# ===Description: ----------------------------------------------------------------------------------
# makes the video sampling, saving one frame every given amount of time determined by the cap_rate 
# parameter.
# ===Arguments: ------------------------------------------------------------------------------------
# dest_folder:  path to the folder where the images will be saved
# video_path:   path to the video file
# cap_rate:     The frame capturing rate: the code captures 1 frame every CAP_RATE seconds
# --------------------------------------------------------------------------------------------------
def run_sampling(dest_folder, video_path, cap_rate):

    cap = cv2.VideoCapture(video_path)
    frameRate = cap.get(5)
    multiplier = int(round(cap_rate * frameRate))
    # name of the next image to be saved
    im_index = 1

    while(cap.isOpened()):

        # the ID of the next frame
        frameID = int(round(cap.get(1)))
        # reading the next frame
        ret, frame = cap.read()

        # checks whether a frame was sucessfully captured
        if(ret == True):
            # this is so that we only capture 1 frame every 1 second
            # if(frameID % math.floor(frameRate) == 0):
            if(frameID % multiplier == 0):
                print(dest_folder+"/"+str(im_index)+'.jpg')
                cv2.imwrite(dest_folder+"/"+str(im_index)+'.jpg',frame)
                im_index+= 1
        else:
        	break


    cap.release()
