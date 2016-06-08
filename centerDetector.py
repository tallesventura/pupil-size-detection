import numpy as np
from matplotlib import pyplot as plt
import math
import cv2


IMG_PATH = "source_images/pic.jpg"

GRADIENT_THRESHOLD_FACTOR = 50.0

# ----calculates the displacement vector
def calc_displacement(x,c):

	vec = x-c
	return (vec/np.linalg.norm(vec))


# ----calculates the gradient's magnitudes
# grads: list with the gradient matrices for the rows and collumns
def calc_grads_mag(grads):

	width = grads[0].shape[1]
	height = grads[0].shape[0]

	nor_grads = np.empty((height,width))

	for i in range(height):
		for j in range(width):
			g = np.array([grads[0][i,j],grads[1][i,j]])
			nor_grads[i,j] = math.sqrt(g[0]**2,g[1]**2)

	return nor_grads

# ----function to calculate the threshold for the gradients
# mags: matrix with the gradients' magnitudes
def calc_dynamic_threshold(mags,stdDevFactor):

	mags_mean, mags_std = cv2.meanStdDev(mags)
	stdDev = mags_std[0] / math.sqrt(mags.shape[0]*mags.shape[1])
	return stdDevFactor * stdDev + mags_mean[0]


# ----function to normalize the gradients
# grads:        list with the gradient matrices for the rows and collumns
# mags: 	   matrix with the gradients' magnitudes
# grad_thresh: gradient threshold
def normalize_grads(grads,mags,grad_thresh):

	width = grads[0].shape[1]
	height = grads[0].shape[0]

	# list of matrices where the normalized gradients will be stored
	norm_grads = np.array([np.empty([height,width]),np.empty([height,width])])

	for i in range(height):
		for j in range(width):
			magnitude = mags[i,j]

			if(magnitude > grad_thresh):
				# gradient for x coordinate
				gX = grads[0][i,j]
				# gradient for y coordinate
				gY = grads[1][i,j]
				# normalized gradient for x coordinate
				nor_grads[0][i,j] = gX/magnitude
				# normalized gradient for y coordinate
				nor_grads[1][i,j] = gY/magnitude
			else:
				nor_grads[0][i,j] = 0.0
				nor_grads[1][i,j] = 0.0


def build_obj_matrix(img):

	width = img.shape[1]
	height = img.shape[0]

	# The matrix of the image's gradients
	grads = np.gradient(img)
	# Matrix of gradients' magnitude
	grads_mag = calc_grads_mag(grads)
	# Calculate the gradient threshold
	grad_thresh = calc_dynamic_threshold(grads_mag,GRADIENT_THRESHOLD_FACTOR)
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


