#!/usr/env python

import cv2
import numpy as np
import os
import math
from matplotlib import pyplot as plt

N_IMAGES = 100
MAX_RADIUS = 80
MIN_RADIUS = 40
PROCESS_POS = False
PROCESS_RADIUS = False
ENABLE_POST_PROC = False

dict_circles = {}
all_circles = []
radius_list = []
images_index = []

# current_folder = os.getcwd()
current_folder = os.getcwd()
imageNames = []
dirname = current_folder + "/circleDetections"


def auto_canny(image, sigma=0.33):
	# compute the median of the single channel pixel intensities
	v = np.median(image)
 
	# apply automatic Canny edge detection using the computed median
	lower = int(max(0, (1.0 - sigma) * v))
	upper = int(min(255, (1.0 + sigma) * v))
	edged = cv2.Canny(image, lower, upper)
 
	# return the edged image
	return edged

# Computes the distance between consecutive circles
def calc_dist_circles(circles):

    out = []
    x1 = circles[0][0]
    y1 = circles[0][1]

    for i in range(1,len(circles)):
        x = circles[i][0]
        y = circles[i][1]
        dx = x1 - x
        dy = y1 - y
        dist = int(math.sqrt(dx**2 + dy**2))
        out.append(dist)
        x1 = x
        y1 = y

    return np.array(out)


def post_process_circles(circles_orig,radius_list):

    out_radius = radius_list.copy()
    circles = np.array(circles_orig).copy()
    radius_mean = int(np.mean(radius_list))
    radius_std = int(np.std(radius_list))
    distances = calc_dist_circles(circles)
    distances_std = int(np.std(distances))

    print('Radius std: ',radius_std)
    print('distances std: ',distances_std)

    if(PROCESS_RADIUS):
        prev_radius = radius_mean
        for i in range(len(radius_list)):
            r = radius_list[i]
            #if(abs(radius_list[i] - prev_radius) > radius_std):
            if(abs(r - prev_radius) > radius_std):
                #print('changed r')
                out_radius[i] = radius_mean
                circles[i][2] = radius_mean
            #prev_radius = radius_list[i]
            prev_radius = r


    if(PROCESS_POS):
        prev_x = circles[0][0]
        prev_y = circles[0][1]
        for i in range(1,len(circles)):
            x = circles[i][0]
            y = circles[i][1]
            if(distances[i-1] > distances_std):
                #print('moved')
                circles[i][0] = round((prev_x + x)/2)
                circles[i][1] = round((prev_y + y)/2)
            #prev_x = circles[i][0]
            #prev_y = circles[i][1]
            prev_x = x
            prev_y = y

    return circles, out_radius


def draw_circles(circles):
   
	for i in range(len(images_index)):
		img_circles = dict_circles.get(str(images_index[i]))
		src_path = current_folder+"/results/"+ str(images_index[i]) + ".jpg"
		dest_path = dirname+'/'+str(images_index[i]) + ".jpg"
		img = cv2.imread(src_path)

		for j in range(len(img_circles)):
			c = (img_circles[j][0],img_circles[j][1])
			r = img_circles[j][2]
			cv2.circle(img, c, r, (0, 255, 0), 2)

		cv2.imwrite(dest_path, img)

	'''
	for i in range(len(circles)):
		src_path = current_folder+"/results/"+ str(images_index[i]) + ".jpg"
		dest_path = dirname+'/'+str(images_index[i]) + ".jpg"
		img = cv2.imread(src_path)
		c = (circles[i][0],circles[i][1])
		r = circles[i][2]
		cv2.circle(img, c, r, (0, 255, 0), 2)
		cv2.imwrite(dest_path, img)
	'''


for i in range(1,N_IMAGES+1):
    number = str(i)

    image_name = current_folder+"/results/"+ number + ".jpg"
    imageNames.append(image_name)
    print(image_name)
    img = cv2.imread(image_name)

    #img = cv2.GaussianBlur(img, (5, 5), 10)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #edges = auto_canny(img)
    print(img.shape)

	
	#dp: This parameter is the inverse ratio of the accumulator resolution to the image resolution (see Yuen et al. for more details). Essentially, the larger the dp gets, the smaller the accumulator array gets.
	#minDist: Minimum distance between the center (x, y) coordinates of detected circles. If the minDist is too small, multiple circles in the same neighborhood as the original may be (falsely) detected. If the minDist is too large, then some circles may not be detected at all.
	#param1: Gradient value used to handle edge detection in the Yuen et al. method.
	#param2: Accumulator threshold value for the cv2.HOUGH_GRADIENT method. The smaller the threshold is, the more circles will be detected (including false circles). The larger the threshold is, the more circles will potentially be returned.
	#minRadius: Minimum size of the radius (in pixels).
	#maxRadius: Maximum size of the radius (in pixels).
    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 2, 100, param1=20, param2=100, minRadius=MIN_RADIUS, maxRadius=MAX_RADIUS)
    #4, 600, param1=50, param2=100, minRadius=40, maxRadius=80)
    #2, 100, param1=20, param2=50, minRadius=40, maxRadius=80)
    #2, 100, param1=20, param2=100, minRadius=40, maxRadius=80)


    cur_img_circles = []
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for c in circles[0,:]:
        #draw the circle
            #cv2.circle(img, (c[0], c[1]), c[2], (0, 255, 0), 2)           
            radius_list.append(c[2])
            cur_img_circles.append(c)
            images_index.append(i)
        #cv2.imwrite(os.path.join(dirname, number + ".jpg"), img)
        dict_circles[number] = cur_img_circles


#circles_raw = np.array(all_circles).copy()
circles_raw = dict_circles.copy()

if(ENABLE_POST_PROC):
    circles_processed, radius_processed = post_process_circles(all_circles,radius_list)
    draw_circles(circles_processed)
    plt.plot(images_index,radius_processed,'r', label='processed')
    plt.plot(images_index,radius_list,'b', label='raw')
    
else:
    draw_circles(circles_raw)
    #plt.plot(images_index,radius_list,'b', label='raw')
    
'''
plt.xlabel('Time')
plt.ylabel('Radius')
plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=1,
           ncol=2, borderaxespad=0.)
plt.show()
'''

