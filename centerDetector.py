import numpy as np
from matplotlib import pyplot as plt
from collections import deque
import math
import cv2


IMG_PATH = "source_images/pic2.jpg"

GRADIENT_THRESHOLD_FACTOR = 50.0
# size of the kernel for the gaussian blur filter
BLUR_KERNEL_SIZE = 5
# height shrinkage ratio
H_RATIO = 0.25
# width shrinkage ratio
W_RATIO = 0.2
# post process threshold
POST_PROCESS_THRESH = 0.97


def cut_eye_pos(in_img):

	in_height = in_img.shape[0]
	in_width = in_img.shape[1]

	# number of rows to be cut from each side
	n_rows = math.floor(in_height * H_RATIO)
	# number of collumns to be cut from each side
	n_col_right = math.floor(in_width * W_RATIO)
	n_col_left = math.floor(in_width * (W_RATIO+0.15))

	# start and end indexes
	xs = n_rows
	xe = in_height - n_rows
	ys = n_col_left
	ye = in_width - n_col_right

	return in_img[xs:xe,ys:ye]



# ----calculates the gradient's magnitudes
# grads: list with the gradient matrices for the rows and collumns
def calc_grads_mag(grads):

	width = grads[0].shape[1]
	height = grads[0].shape[0]

	nor_grads = np.empty((height,width))

	for i in range(height):
		for j in range(width):
			g = np.array([grads[0][i,j],grads[1][i,j]])
			nor_grads[i,j] = math.sqrt(g[0]**2 + g[1]**2)

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
	norm_grads = np.array([np.empty((height,width)),np.empty((height,width))])

	for i in range(height):
		for j in range(width):
			magnitude = mags[i,j]

			if(magnitude > grad_thresh):
				# gradient for x coordinate
				gX = grads[0][i,j]
				# gradient for y coordinate
				gY = grads[1][i,j]
				# normalized gradient for x coordinate
				norm_grads[0][i,j] = gX/magnitude
				# normalized gradient for y coordinate
				norm_grads[1][i,j] = gY/magnitude
			else:
				norm_grads[0][i,j] = 0.0
				norm_grads[1][i,j] = 0.0

	return norm_grads


def test_possible_centers(x, y, weights, gx, gy, out):

	for cx in range(out.shape[0]):
		for cy in range(out.shape[1]):
			if(x == cx and y == cy):
				continue

			# displacement vector components
			dx = x - cx
			dy = y - cy

			# normalizing the displacement vector
			magnitude = math.sqrt(dx**2 + dy**2)
			dx /= magnitude
			dy /= magnitude

			#calculating the dot product
			dot = dx*gx + dy*gy
			dot = max(0.0,dot)

			out[cx,cy] = (dot**2)*weights[cx,cy]

	return out 


def inMat(p, rows, cols):
	return p[0] >= 0 and p[0] < rows and p[1] >= 0 and p[1] < cols 


def killEdges(mat):

	height = mat.shape[0]
	width = mat.shape[1]

	mask = np.empty((height,width))
	mask[:] = 255

	que = deque([(0,0)])

	while(len(que) != 0):
		p = popleft()
		x = p[0]
		y = p[1]

		if(mat[x,y] == 0.0):
			continue

		np = (x+1,y)
		if(inMat(np,height,width)):
			que.append(np)
		np = (x-1,y)
		if(inMat(np,height,width)):
			que.append(np)
		np = (x,y+1)
		if(inMat(np,height,width)):
			que.append(np)
		np = (x,y-1)
		if(inMat(np,height,width)):
			que.append(np)


		mat[x,y] = 0.0
		mask[x,y] = 0

	return mask, mat


def build_obj_matrix(img):

	width = img.shape[1]
	height = img.shape[0]

	# The matrix of the image's gradients
	print("calculating the gradients")
	grads = np.gradient(img)
	# Matrix of gradients' magnitude
	print("calculating the gradients' magnitudes")
	grads_mag = calc_grads_mag(grads)
	# Calculate the gradient threshold
	print("calculating the gradient threshold")
	grad_thresh = calc_dynamic_threshold(grads_mag,GRADIENT_THRESHOLD_FACTOR)
	# number of pixels in the image
	n_pixels = width * height
	# normalizing the gradients
	print("normalizing the gradients")
	grads = normalize_grads(grads,grads_mag,grad_thresh)

	# Smoothing the original image
	print("smoothing the original image")
	weights = cv2.GaussianBlur(img,(BLUR_KERNEL_SIZE,BLUR_KERNEL_SIZE),0)
	# inverting the blured image
	print("inverting the smoothed image")
	for i in range(height):
		for j in range(width):
			weights[i,j] = 255 - weights[i,j]

	# the matrix of sums
	out_sum = np.zeros((height,width))

	# calculate the matrix of sums (objective function)
	print("calculating the sums")
	for i in range(weights.shape[0]):
		for j in range(weights.shape[1]):
			gX = grads[0][i,j]
			gY = grads[1][i,j]
			if(gX == 0.0 and gY == 0.0):
				continue
			out_sum = test_possible_centers(i,j,weights,gX,gY,out_sum)

	print("finished calculating the sums")
	n_grads = weights.shape[0] * weights.shape[1]
	out_sum *= 1/(n_grads)


	minVal, maxVal, minPos, maxPos = cv2.minMaxLoc(out_sum)
	print("Max pos antes: ",maxPos)
	print("Max val antes: ",maxVal)

	print("post proessing")
	floodThresh = maxVal * POST_PROCESS_THRESH
	ret,out = cv2.threshold(out_sum,floodThresh,0.0,cv2.THRESH_TOZERO)

	mask, out = killEdges(out)
	minVal, maxVal, minPos, maxPos = cv2.minMaxLoc(out_sum,mask)

	print("Max pos depois: ",maxPos)
	print("Max val depois: ",maxVal)

# =====================================================================================
img = cv2.imread(IMG_PATH,cv2.IMREAD_GRAYSCALE)
print("original img: ",img.shape)

eye = cut_eye_pos(img)
eye_scaled = cv2.resize(eye,(50,int((50.0/eye.shape[1])*eye.shape[0])))
print("eye: ",eye.shape)
print("eye_scaled",eye_scaled.shape)

build_obj_matrix(eye_scaled)



plt.subplot(131)
plt.imshow(img)
plt.subplot(132)
plt.imshow(eye)
plt.subplot(133)
plt.imshow(eye_scaled)
plt.show()


