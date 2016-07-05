#!/usr/env python

import cv2
import numpy as np
import os
import math
import random
import time
from matplotlib import pyplot as plt
from collections import deque

N_IMAGES = 100
# The maximun radius for the HoughCircles function
MAX_RADIUS = 80
# The minimun radius for the HoughCircles function
MIN_RADIUS = 30
ENABLE_POST_PROC = False
# The frame capturing rate: the code captures 1 frame every CAP_RATE seconds
CAPTURE_RATE = 0.5
PERCENTAGE_BLACK_THRESHOLD = 10

MAX_ITER_LS = 5
THRESH_IT_NOT_IMPROV = 40
LOWER_P1 = 8
UPPER_P1 = 300
LOWER_P2 = 30
UPPER_P2 = 600
LOWER_MIN_DIST = 100
UPPER_MIN_DIST = 700
MAX_DP = 10

#dict_circles = {}
images_index = []
radius_list = []

current_folder = os.getcwd()
imageNames = []
dirname = current_folder + "/circleDetections"


def get_radius_list(circles_dict):
	keys = sorted(list(circles_dict.keys()))
	list_radius = []

	for i in range(len(keys)):
		list_radius.append(circles_dict[keys[i]][2])

	return list_radius


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


def select_circles(circs):
	for c in circs:
		r = c[2]
		x = c[0]
		y = c[1]
		



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
	#n_frames = int(5*(1/CAPTURE_RATE))
	n_frames = min(int(round(len(list_areas)*0.045)),len(list_areas))
	#print("n_frames:",n_frames)
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


def generate_circles(dp, min_dist, p1, p2, n_imgs = N_IMAGES):
	# Reading the images and finding the circles
	
	dict_circles = {}
	for i in range(1,n_imgs+1):
		number = str(i)

		image_name = current_folder+"/results/gray scale/"+ number + ".jpg"
		imageNames.append(image_name)
		#print(image_name)
		img = cv2.imread(image_name,cv2.IMREAD_GRAYSCALE)


		#img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		#print(img.shape)


		#dp: This parameter is the inverse ratio of the accumulator resolution to the image resolution (see Yuen et al. for more details). Essentially, the larger the dp gets, the smaller the accumulator array gets.
		#minDist: Minimum distance between the center (x, y) coordinates of detected circles. If the minDist is too small, multiple circles in the same neighborhood as the original may be (falsely) detected. If the minDist is too large, then some circles may not be detected at all.
		#param1: Gradient value used to handle edge detection in the Yuen et al. method.
		#param2: Accumulator threshold value for the cv2.HOUGH_GRADIENT method. The smaller the threshold is, the more circles will be detected (including false circles). The larger the threshold is, the more circles will potentially be returned.
		#minRadius: Minimum size of the radius (in pixels).
		#maxRadius: Maximum size of the radius (in pixels).
		circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, dp, min_dist, param1=p1, param2=p2, minRadius=MIN_RADIUS, maxRadius=MAX_RADIUS)
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

	return dict_circles
#============================================================================================================


def local_search(sol,obj,n_imgs):

	cur_sol = sol.copy()
	cur_obj = obj
	best_sol = sol.copy()
	best_obj = obj
	improved = False

	ratio = random.random() + 0.1
	inc_dec = random.randint(0,1)
	pos = random.randint(0,3)

	for i in range(1,MAX_ITER_LS+1):
		n = cur_sol[pos]
		if(inc_dec == 0):			
			if(pos == 0):
				cur_sol[pos] =  max(int(n - (n*ratio)/i),1)
			elif(pos == 1):
				cur_sol[pos] =  max(int(n - (n*ratio)/i),LOWER_MIN_DIST-1)
			elif(pos == 2):
				cur_sol[pos] =  max(int(n - (n*ratio)/i),LOWER_P1-1)
			elif(pos == 3):
				cur_sol[pos] =  max(int(n - (n*ratio)/i),LOWER_P2-1)
		else:
			cur_sol[pos] = int(n + (n*ratio)/i)

		circles = generate_circles(cur_sol[0],cur_sol[1],cur_sol[2],cur_sol[3],n_imgs)
		circles = select_circles(circles)
		cur_obj = len(circles)

		if(cur_obj >= best_obj):
			improved = True
			best_obj = cur_obj
			best_sol = cur_sol.copy()
		elif(improved == True):
			break
			


	return best_sol


def parameter_tunning(n_iter, sol, n_imgs):

	cur_sol = sol.copy()
	best_sol = sol.copy()
	circles = generate_circles(sol[0],sol[1],sol[2],sol[3],n_imgs)
	circles = select_circles(circles)
	cur_obj = len(circles)
	best_obj = cur_obj
	pos = random.randint(0,3)
	hist_pos = deque([pos])
	n_it_not_improved = 0

	for i in range(n_iter):
		print("Iteration ", i)
		inc_dec = random.randint(0,1)
		ratio = random.randrange(1,6)/10
		while(hist_pos.count(pos) > 0):
			pos = random.randint(0,3)

		hist_pos.append(pos)
		if(len(hist_pos) > 0):
			hist_pos.popleft()
		
		# Disturbance------------------------------------------------------------------
		cur_sol = best_sol.copy()
		n = cur_sol[pos]
		if(inc_dec == 1):
			cur_sol[pos] += int(n*ratio)
		else:
			if(pos == 0):
				cur_sol[pos] =  max(int(n - (n*ratio)),1)
			elif(pos == 1):
				cur_sol[pos] =  max(int(n - (n*ratio)),LOWER_MIN_DIST-1)
			elif(pos == 2):
				cur_sol[pos] =  max(int(n - (n*ratio)),LOWER_P1-1)
			elif(pos == 3):
				cur_sol[pos] =  max(int(n - (n*ratio)),LOWER_P2-1)
		#--------------------------------------------------------------------------------

		# Local search
		cur_sol = local_search(cur_sol,cur_obj,n_imgs)

		circles = generate_circles(cur_sol[0],cur_sol[1],cur_sol[2],cur_sol[3],n_imgs)
		circles = select_circles(circles)
		cur_obj = len(circles)
		print("n_images: ", cur_obj)
		print(cur_sol)

		# Acceptance
		if(cur_obj > best_obj):
			best_obj = cur_obj
			best_sol = cur_sol.copy()
			n_it_not_improved = 0
		else:
			n_it_not_improved += 1

		if(n_it_not_improved >= THRESH_IT_NOT_IMPROV):
			break

	return best_sol



print("Tunning parameters")
time_before = time.clock()
#sol = parameter_tunning(50,[2,100,20,100],12)
time_after = time.clock()
print("parameter tunning completed in: ",time_after - time_before)
#print("dp: ",sol[0]," minDist: ",sol[1]," p1: ",sol[2]," p2: ",sol[3])
print("Generating circles")
#circles_raw = generate_circles(sol[0],sol[1],sol[2],sol[3],100)
circles_raw = generate_circles(3,100,32,100,100)
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
