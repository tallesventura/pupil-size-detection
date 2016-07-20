import cv2
from PyQt4 import QtCore



class VideoProcessor(QtCore.QThread):

    def __init__(self, parent=None):
        super(VideoProcessor, self).__init__(parent)
        self.cap = None
        self.notifyProgress = QtCore.pyqtSignal(int)

    # ===Description: ----------------------------------------------------------------------------------
    # makes the video sampling, saving one frame every given amount of time determined by the cap_rate
    # parameter.
    # ===Arguments: ------------------------------------------------------------------------------------
    # dest_folder:  path to the folder where the images will be saved
    # video_path:   path to the video file
    # cap_rate:     The frame capturing rate: the code captures 1 frame every CAP_RATE seconds
    # --------------------------------------------------------------------------------------------------
    def run(self, dest_folder, video_path, cap_rate):

        self.cap = cv2.VideoCapture(video_path)
        frameRate = self.cap.get(5)
        multiplier = int(round(cap_rate * frameRate))
        # name of the next image to be saved
        im_index = 1

        while(self.cap.isOpened()):

            # the ID of the next frame
            frameID = int(round(self.cap.get(1)))
            # reading the next frame
            ret, frame = self.cap.read()

            # checks whether a frame was sucessfully captured
            if(ret == True):
                # this is so that we only capture 1 frame every 1 second
                # if(frameID % math.floor(frameRate) == 0):
                if(frameID % multiplier == 0):
                    print(dest_folder+"/"+str(im_index)+'.jpg')
                    cv2.imwrite(dest_folder+"/"+str(im_index)+'.jpg',frame)
                    self.notifyProgress.emit(im_index)
                    im_index+= 1
            else:
                break


        self.cap.release()
