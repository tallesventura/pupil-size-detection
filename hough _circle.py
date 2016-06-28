#!/usr/env python

import cv2
import numpy as np
import os
import math
from matplotlib import pyplot as plt

N_IMAGES = 100
# The maximun radius for the HoughCircles function
MAX_RADIUS = 80
# The minimun radius for the HoughCircles function
MIN_RADIUS = 40
ENABLE_POST_PROC = False
# The frame capturing rate: the code captures 1 frame every CAP_RATE seconds
CAPTURE_RATE = 0.5
PERCENTAGE_BLACK_THRESHOLD = 10

dict_circles = {}
images_index = []
radius_list = []

# current_folder = os.getcwd()
current_folder = os.getcwd()
imageNames = []
dirname = current_folder + "/circleDetections"


def get_radius_list(circles_dict):
    keys = sorted(list(circles_dict.keys()))
    list_radius = []

    for i in range(len(keys)):
        list_radius.append(circles_dict[keys[i]][2])

    return list_radius


# Computes the distance between consecutive circles
def calc_dist_circles(circles):

    out = []
    x1 = circles[0][0]
    y1 = circles[0][1]

    for i in range(1, len(circles)):
        x = circles[i][0]
        y = circles[i][1]
        dx = x1 - x
        dy = y1 - y
        dist = int(math.sqrt(dx**2 + dy**2))
        out.append(dist)
        x1 = x
        y1 = y

    return np.array(out)

# circles: 		dictionary with the name of the images as keys and the circle parameters as values
# dest_folder:	path to the folder where the images will be saved
def draw_circles(circles, dest_folder):
    keys = list(circles.keys())
    for k in keys:
        img_circles = circles.get(k)
        src_path = current_folder+"/results/gray scale/"+ str(k) + ".jpg"
        dest_path = dest_folder+'/'+str(k) + ".jpg"
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


# circle:	list with a circle's parameters (x,y,radius)
def count_pixels(img, circle):
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

    black = 0
    white = 0
    for i in range(h):
        for j in range(w):
            if(img_box[i,j] == 0):
                black+= 1
            else:
                white+= 1

    return black, white


# circs: dictionary with the name of the images as keys and the circle parameters as values
def select_circles(circs):

    out = {}
    keys = list(circs.keys())
    for k in keys:
        img_circles = circs.get(k)
        src_path = current_folder+"/results/binary/"+ str(k) + ".jpg"
        img = cv2.imread(src_path,cv2.IMREAD_GRAYSCALE)
        blackP_list = []
        whiteP_list = []
        circles = []

        for j in range(len(img_circles)):
            black, white = count_pixels(img,img_circles[j])
            blackP_list.append(black)
            whiteP_list.append(white)

        blackP_list = np.array(blackP_list)
        index_max = blackP_list.argmax()
        b = blackP_list[index_max]
        w = whiteP_list[index_max]
        total_pixels = b + w
        percentage_black = (100*b)/total_pixels
        if(percentage_black >= PERCENTAGE_BLACK_THRESHOLD):
            c = img_circles[index_max]
            out[k] = c

    return out


# list_areas: list with the areas of the circles
def get_baseline_area(list_areas):
    n_frames = int(5*(1/CAPTURE_RATE))
    print("n_frames:",n_frames)
    l = list_areas[:n_frames]
    return np.mean(l)


# list_areas: list with the areas of the circles
def get_percentage_area(list_areas, baseline_area):

    out = []
    for a in list_areas:
        out.append((100*a)/baseline_area)

    return out


# list_radius: list with the radius of the circles
def get_areas(list_radius):
    out = []
    for r in list_radius:
        out.append(3.14 * (r**2))

    return out


# Reading the images and finding the circles
#=============================================================================================================
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
        dict_circles[i] = cur_img_circles
#============================================================================================================


circles_raw = dict_circles.copy()
print("Selecting the best circle")
circs = select_circles(circles_raw)
indexes = sorted(list(circs.keys()))
print("n_images: ", len(indexes))
list_radius = get_radius_list(circs)
list_areas = get_areas(list_radius)
baseline_area = get_baseline_area(list_areas)
print("baseline area: ", baseline_area)
percentage_areas = get_percentage_area(list_areas, baseline_area)


if(ENABLE_POST_PROC):
    print("post-processing the circles")
    circles_processed, radius_processed = post_process_circles(circs)
    print("drawing the circles")
    draw_circles(circles_processed,dirname)
    print("plotting the graph")
    plt.plot(indexes,radius_processed,'r', label='processed')
    plt.plot(indexes,get_radius_list(circs),'b', label='raw')
else:
    print("drawing the circles")
    draw_circles(circs,dirname)
    print("plotting the graph")
    plt.plot(indexes,percentage_areas,'b', label='raw')

plt.xlabel("Time (sec.)")
plt.ylabel('% \of Baseline Area')
plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=1,
           ncol=2, borderaxespad=0.)
plt.show()

