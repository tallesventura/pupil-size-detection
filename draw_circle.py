import cv2
import numpy as np
import os

class DrawWindow:

    def __init__(self):
        self.drawing = False
        self.ix = -1
        self.iy = -1
        self.img = None

    #mouse callback function
    def draw_circle(self, event, x, y, flags, param):

        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True
            self.ix = x
            self.iy = y

        elif event == cv2.EVENT_MOUSEMOVE:
            if self.drawing == True:
                cv2.circle(self.img, (x, y), 5, (0, 0, 255), -1)

        elif event == cv2.EVENT_LBUTTONUP:
            self.drawing = False
            #cv2.circle(self.img, (x,y), 20, (0, 0, 255), -1)

    def show(self, path):
        self.img = cv2.imread(path)
        cv2.namedWindow("window")
        cv2.setMouseCallback("window", self.draw_circle)

        while(1):
            cv2.imshow('window', self.img)
            k = cv2.waitKey(1) & 0xFF
            if k == ord('s'):
                # list_name = list(os.path.splitext(path))
                # list_name.insert(1, "_draw")
                # draw_file = ''.join(list_name)
                cv2.imwrite(path, self.img)
            elif k == ord('q'):
                break

        cv2.destroyAllWindows()

if __name__ == "__main__":
    t = DrawWindow()
    t.show("/home/marcosfe/Projects/pupil-size-detection/ord.jpg")