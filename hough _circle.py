#!/usr/env python

import cv2
import numpy as np
import os
import math
from matplotlib import pyplot as plt

N_IMAGES = 50
MAX_RADIUS = 80
MIN_RADIUS = 40
PROCESS_POS = False
PROCESS_RADIUS = False
ENABLE_POST_PROC = True

dict_circles = {}
images_index = []
radius_list = []

# current_folder = os.getcwd()
current_folder = os.getcwd()
imageNames = []
dirname = current_folder + "/circleDetections"


def get_radius_list(circles_dict):
    circles = list(circles_dict.values())
    list_radius = []

    for i in range(len(circles)):
        list_radius.append(circles[i][2])

    return list_radius


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


def post_process_circles(circles_dict):

    out_dict = circles_dict.copy()
    circles = list(circles_dict.values())
    list_radius = get_radius_list(circles_dict)
    list_centers = []

    for i in range(len(images_index)):
        x = circles[i][0]
        y = circles[i][1]
        list_centers.append((x,y))

    out_radius = list_radius.copy()
    radius_mean = int(np.mean(list_radius))
    radius_std = int(np.std(list_radius))


    print('Radius std: ',radius_std)

    prev_radius = radius_mean
    for i in range(len(list_radius)):
        r = list_radius[i]
        c = circles_dict[str(i+1)]
        #if(abs(radius_list[i] - prev_radius) > radius_std):
        if(abs(r - prev_radius) > radius_std):
            #print('changed r')
            out_radius[i] = prev_radius
            c[2] = prev_radius
            out_dict[str(i)] = c
        #prev_radius = radius_list[i]
        prev_radius = r


    return out_dict, out_radius


def draw_circles(circles,dest_folder):

    for i in range(len(images_index)):
        img_circles = circles.get(str(images_index[i]))
        src_path = current_folder+"/results/binary/"+ str(images_index[i]) + ".jpg"
        dest_path = dest_folder+'/'+str(images_index[i]) + ".jpg"
        img = cv2.imread(src_path)

        if(type(img_circles) is list):
            for j in range(len(img_circles)):
                c = (img_circles[j][0],img_circles[j][1])
                r = img_circles[j][2]
                cv2.circle(img, c, r, (0, 255, 0), 2)
        else:
            c = (img_circles[0],img_circles[1])
            r = img_circles[2]
            cv2.circle(img, c, r, (0, 255, 0), 2)

        cv2.imwrite(dest_path, img)



def count_black_pixels(img, circle):
    
    x = circle[1]
    y = circle[0]
    r = circle[2]
    xs = x-r
    xe = x+r+1
    ys = y-r
    ye = y+r+1

    img_box = np.array(img[xs:xe,ys:ye])
    h = img_box.shape[0]
    w = img_box.shape[1]

    count = 0
    for i in range(h):
        for j in range(w):
            if(img_box[i,j] == 0):
                count+= 1

    return count



def select_circles(circs):

    out = {}
    for i in range(len(images_index)):
        img_circles = circs.get(str(images_index[i]))
        src_path = current_folder+"/results/binary/"+ str(images_index[i]) + ".jpg"
        img = cv2.imread(src_path,cv2.IMREAD_GRAYSCALE)
        pCount_list = []
        circles = []

        for j in range(len(img_circles)):
            pCount_list.append(count_black_pixels(img,img_circles[j]))

        pCount_list = np.array(pCount_list)

        c = img_circles[pCount_list.argmax()]
        out[str(images_index[i])] = c

    return out
        



for i in range(1,N_IMAGES+1):
    number = str(i)

    image_name = current_folder+"/results/gray scale/"+ number + ".jpg"
    imageNames.append(image_name)
    print(image_name)
    img = cv2.imread(image_name)


    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print(img.shape)

	
	#dp: This parameter is the inverse ratio of the accumulator resolution to the image resolution (see Yuen et al. for more details). Essentially, the larger the dp gets, the smaller the accumulator array gets.
	#minDist: Minimum distance between the center (x, y) coordinates of detected circles. If the minDist is too small, multiple circles in the same neighborhood as the original may be (falsely) detected. If the minDist is too large, then some circles may not be detected at all.
	#param1: Gradient value used to handle edge detection in the Yuen et al. method.
	#param2: Accumulator threshold value for the cv2.HOUGH_GRADIENT method. The smaller the threshold is, the more circles will be detected (including false circles). The larger the threshold is, the more circles will potentially be returned.
	#minRadius: Minimum size of the radius (in pixels).
	#maxRadius: Maximum size of the radius (in pixels).
    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 2, 100, param1=20, param2=100, minRadius=MIN_RADIUS, maxRadius=MAX_RADIUS)
    #2, 100, param1=20, param2=100, minRadius=40, maxRadius=80)
    #2, 30, param1=20, param2=130, minRadius=40, maxRadius=80)
    #2, 30, param1=20, param2=115, minRadius=40, maxRadius=80)


    cur_img_circles = []
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for c in circles[0,:]:
            cur_img_circles.append(c)
            
        images_index.append(i)
        dict_circles[number] = cur_img_circles


circles_raw = dict_circles.copy()

if(ENABLE_POST_PROC):
    circs = select_circles(circles_raw)
    circles_processed, radius_processed = post_process_circles(circs)
    draw_circles(circles_processed,dirname)
    plt.plot(images_index,radius_processed,'r', label='processed')
    plt.plot(images_index,get_radius_list(circs),'b', label='raw')
    plt.show()
    
else:
    circs = select_circles(circles_raw)
    draw_circles(circles_raw,current_folder+"/results")
    draw_circles(circs,dirname)
    #plt.plot(images_index,radius_list,'b', label='raw')
    


'''
plt.xlabel('Time')
plt.ylabel('Radius')
plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=1,
           ncol=2, borderaxespad=0.)
plt.show()
'''

