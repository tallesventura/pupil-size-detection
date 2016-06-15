#!/usr/env python

import cv2
import numpy as np
import os

N_IMAGES = 111

# current_folder = os.getcwd()
current_folder = os.getcwd()
imageNames = []
dirname = current_folder + "/circleDetections"

for i in range(1,N_IMAGES+1):
    number = str(i)

    image_name = current_folder+"/results" + "/"+ number + ".jpg"
    imageNames.append(image_name)
    print(image_name)
    img = cv2.imread(image_name)
    img = cv2.GaussianBlur(img, (5, 5), 10)

    print(img.shape)

    gimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# cv2.imshow("gray",gimg)
# cv2.waitKey(0) & 0xFF
	
	#dp: This parameter is the inverse ratio of the accumulator resolution to the image resolution (see Yuen et al. for more details). Essentially, the larger the dp gets, the smaller the accumulator array gets.
	#minDist: Minimum distance between the center (x, y) coordinates of detected circles. If the minDist is too small, multiple circles in the same neighborhood as the original may be (falsely) detected. If the minDist is too large, then some circles may not be detected at all.
	#param1: Gradient value used to handle edge detection in the Yuen et al. method.
	#param2: Accumulator threshold value for the cv2.HOUGH_GRADIENT method. The smaller the threshold is, the more circles will be detected (including false circles). The larger the threshold is, the more circles will potentially be returned.
	#minRadius: Minimum size of the radius (in pixels).
	#maxRadius: Maximum size of the radius (in pixels).
    circles = cv2.HoughCircles(gimg, cv2.HOUGH_GRADIENT, 1, 600, param1=40, param2=15, minRadius=40, maxRadius=96)

    #2 = 18



    if circles is not None:
        circles = np.uint16(np.around(circles))
        for c in circles[0,:]:
        #draw the circle
         cv2.circle(img, (c[0], c[1]), c[2], (0, 255, 0), 2)

        cv2.imwrite(os.path.join(dirname, number + ".jpg"), img)
        # cv2.imshow("detected circles", img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

