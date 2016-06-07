#!/usr/env python

import cv2
import numpy as np
import os

current_folder = os.getcwd()
image_name = current_folder+"\\source_images\\1.jpg"

img = cv2.imread(image_name)
img = cv2.GaussianBlur(img, (5, 5), 10)

print(img.shape)

gimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# cv2.imshow("gray",gimg)
# cv2.waitKey(0) & 0xFF

circles = cv2.HoughCircles(gimg, cv2.HOUGH_GRADIENT, 1, 20, param1=35, param2=20, minRadius=0, maxRadius=0)

if circles is not None:
    circles = np.uint16(np.around(circles))
    for c in circles[0,:]:
    #draw the circle
        cv2.circle(img, (c[0], c[1]), c[2], (0, 255, 0), 2)

    cv2.imshow("detected circles", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

else:
    print("Lascou")
