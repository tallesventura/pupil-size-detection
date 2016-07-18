from matplotlib import pyplot as plt 
import parameter_selector
import numpy as np
import circles_utils
import preProcessing
import time
import cv2
import graph_builder
import videoProcessor

n_images = 20


#print("Tunning parameters")
orig_path = "/Users/talles/Documents/Summer project/pupil size detection/pupil-size-detection/source_images/videoCapTest"
img_gray = cv2.imread("/Users/talles/Documents/Summer project/pupil size detection/pupil-size-detection/results/gray scale/17.jpg",cv2.IMREAD_GRAYSCALE)
img_bin = cv2.imread("/Users/talles/Documents/Summer project/pupil size detection/pupil-size-detection/results/binary/17.jpg",cv2.IMREAD_GRAYSCALE)
path_gray = "/Users/talles/Documents/Summer project/pupil size detection/pupil-size-detection/results/gray scale"
path_bin = "/Users/talles/Documents/Summer project/pupil size detection/pupil-size-detection/results/binary"
path_dest = "/Users/talles/Documents/Summer project/pupil size detection/pupil-size-detection/circleDetections"


videoProcessor.run_sampling("/Users/talles/Documents/Summer project/pupil size detection/pupil-size-detection/source_images/videoCapTest","/Users/talles/Documents/Summer project/pupil size detection/pupil-size-detection/source_images/v2.mp4",1.0)
#print("finished sampling the video")

preProcessing.run(np.arange(1,107),orig_path,path_gray,path_bin)

time_before = time.clock()
sol = parameter_selector.ils(img_gray,img_bin,[1, 213, 30, 10],27,70)
time_after = time.clock()
print("parameter tunning completed in: ",time_after - time_before)
print(sol)
print("Generating circles")
circles_raw = circles_utils.generate_circles(sol,path_gray,np.arange(1,n_images+1),27,70)


'''
circs = {}
for i in range(1,n_images+1):
	print(i)
	img_gray = cv2.imread("/Users/talles/Documents/Summer project/pupil size detection/pupil-size-detection/results/gray scale/"+str(i)+".jpg",cv2.IMREAD_GRAYSCALE)
	img_bin = cv2.imread("/Users/talles/Documents/Summer project/pupil size detection/pupil-size-detection/results/binary/"+str(i)+".jpg",cv2.IMREAD_GRAYSCALE)
	sol = parameter_selector.ils(img_gray,img_bin,[1, 213, 30, 10],27,80)
	circles_raw = circles_utils.generate_circles(sol,path_gray,[i],27,80)	
	circs[i] = circles_utils.select_circle(img_bin,circles_raw.get(i))
	circles_utils.draw_circles(circles_raw,path_gray,path_dest)
'''

print("Selecting the best circle")
circs = circles_utils.select_circles(n_images,circles_raw,path_bin)
print("len(circles): ",len(circles_raw))
indexes = sorted(list(circs.keys()))
circles_utils.draw_circles(circs,path_gray,path_dest)
print("n_images: ", len(indexes))
list_radius = circles_utils.get_radius_list(circs)
list_areas = circles_utils.get_areas(list_radius)
baseline_area = circles_utils.get_baseline_area(list_areas,5)
print("baseline area: ", baseline_area)
percentage_areas = circles_utils.get_percentage_area(list_areas, baseline_area)

print("plotting the graph")
plt.plot(np.array(indexes),percentage_areas,'b', label='470 nm, 8 uW',linewidth=3.0)

plt.xlabel("Time (sec.)")
plt.ylabel('% \of Baseline Area')
plt.axis([0,int(n_images),0,250])
plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=1,
           ncol=2, borderaxespad=0.)
plt.show()
"""
#===================================================================

indexes = []
areas = []

for i in range(4):
	time_before = time.clock()
	sol = parameter_selector.ils(img_gray,img_bin,[1, 213, 30, 10],27,80)
	time_after = time.clock()
	print("parameter tunning completed in: ",time_after - time_before)
	print(sol)
	print("Generating circles")

	circles_raw = circles_utils.generate_circles(sol,path_gray,np.arange(1,15),27,80)
	print("Selecting the best circle")
	circs = circles_utils.select_circles(40,circles_raw,path_bin)
	print("len(circles): ",len(circles_raw))
	indexes.append(sorted(list(circs.keys())))
	circles_utils.draw_circles(circs,path_gray,path_dest)
	print("n_images: ", len(indexes))
	list_radius = circles_utils.get_radius_list(circs)
	list_areas = circles_utils.get_areas(list_radius)
	baseline_area = circles_utils.get_baseline_area(list_areas,5)
	print("baseline area: ", baseline_area)
	areas.append(circles_utils.get_percentage_area(list_areas, baseline_area))


print("ploting the graph")
x1 = indexes[0]
x2 = indexes[1]
x3 = indexes[2]
x4 = indexes[3]
y1 = areas[0]
y2 = areas[1]
y3 = areas[2]
y4 = areas[3]
graph_builder.plot_graph(x1,y1,x2,y2,x3,y3,x4,y4,'1','2','3','4')
"""
