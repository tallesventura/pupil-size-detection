import numpy as np 
import cv2

# circles_dict: dictionary where the keys are the name of the image and the values
#     are the parameters of the circle found on that image
def get_radius_list(circles_dict):
	keys = sorted(list(circles_dict.keys()))
	list_radius = []

	for i in range(len(keys)):
		list_radius.append(circles_dict[keys[i]][2])

	return list_radius


# circles: 		  dictionary with the name of the images as keys and the circle parameters as values
# src_path:     path to the folder where the images original images are
# dest_folder:	path to the folder where the images will be saved
def draw_circles(circles, src_path, dest_folder):
	keys = list(circles.keys())
	for k in keys:
		img_circles = circles.get(k)
		src_path = src_path + '/' + str(k) + ".jpg"
		dest_path = dest_folder+'/'+str(k) + ".jpg"
		img = cv2.imread(src_path)

		c = (img_circles[0],img_circles[1])
		r = img_circles[2]
		cv2.circle(img, c, r, (0, 255, 0), 2)

		cv2.imwrite(dest_path, img)


# circle: list with a circle's parameters (x,y,radius)
def count_pixels(img, circle):
  x = circle[1]
  y = circle[0]
  r = circle[2]
  xs = max(0,x-r)
  xe = min(img.shape[0]-1,x+r+1)
  ys = max(0,y-r)
  ye = min(img.shape[1]-1,y+r+1)
  #print(x,y,r)
  #print("xs:",xs,"xe:",xe,"ys:",ys,"ye",ye)

  img_box = np.array(img[xs:xe,ys:ye])
  #print(img_box.shape)
  h = img_box.shape[0]
  w = img_box.shape[1]
  total_pixels = h*w

  black = 0
  white = 0
  for i in range(h):
      for j in range(w):
          if(img_box[i,j] == 0):
              black+= 1
          else:
            white+= 1

  percent_black = (100*black)/total_pixels
  percent_white = (100*white)/total_pixels


  return percent_black, percent_white


# circles: list of circles
def select_circle(img,circles):
  best_circle = circles[0]
  best_percent_black = 0.0
  for c in circles:
    black, white = count_pixels(img,c)
    if(black > best_percent_black):
      best_circle = c

  return best_circle


# list_areas: list with the areas of the circles
# n_images:   number of images that will be used to calculate the baseline area
def get_baseline_area(list_areas,n_images):
	l = list_areas[:n_images]
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

