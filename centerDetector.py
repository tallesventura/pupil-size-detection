import numpy as np
from matplotlib import pyplot as plt
import math
import cv2


IMG_PATH = "pic.jpg"


def calc_displacement(x,c):

	vec = x-c
	return (vec/np.linalg.norm(vec))


def calc_obj(c,grads):

	total = 0;
	for i in range(grads[1].shape[0]):
		for j in range(grads[1].shape[1]):

			xi = np.array([i,j])

			# displacement vector
			d = calc_displacement(np.array([i,j]),c)

			# gradient at the position (i,j)
			g = np.array([grads[0][i,j],grads[1][i,j]])
			# normalized gradient
			norm_g = np.linalg.norm(g-xi)

			total += max(0.0,np.dot(d,g))**2

	return total


def build_obj_matrix(img):

	width = img.shape[1]
	height = img.shape[0]

	# The matrix of the image's gradients
	grads = np.gradient(img)

	# number of pixels in the image
	n_pixels = width * height


	# The matrix where the values of the objective function for earch pixel as a center will
	# be stored
	opt_mat = np.empty((height,width))

	for i in range(height):
		for j in range(width):
			opt_mat[i,j] = calc_obj(np.array([i,j]),grads)

	return (1/n_pixels)*opt_mat

# =====================================================================================
img = cv2.imread(IMG_PATH,cv2.IMREAD_GRAYSCALE)

mat = build_obj_matrix(img)

plt.plot(mat)
plt.show()

