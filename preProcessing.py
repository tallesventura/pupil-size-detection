#! /usr/env python

import numpy as np
import cv2
import math
import os
from matplotlib import pyplot as plt


# height shrinkage ratio
H_RATIO = 0.13
# width shrinkage ratio
W_RATIO = 0.1
N_IMAGES = 242

def createClare(img):

    #get path

    image = img

    channelB = image[: , :, 0]
    channelG = image[: , :, 1]
    channelR = image[: , :, 2]

    # create a CLAHE object(Contrast Limited Adaptive Histogram Equalization)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cl1 = clahe.apply(channelB)
  #  cv2.imwrite('bluechannel.jpg', cl1)

    clahe1 = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cl2 = clahe1.apply(channelG)

   # cv2.imwrite(imageID, cl2)

    clahe2 = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cl3 = clahe2.apply(channelR)
    #cv2.imwrite('redChannel.jpg', cl3)

    result = cv2.merge((cl1, cl2, cl3))

    # cv2.imwrite("channelb.jpeg", cl1)
    # cv2.imwrite("channelg.jpeg", cl2)
    # cv2.imwrite("channelr.jpeg", cl3)
    #
    # cv2.imwrite("result.jpeg", result)

    return result

def hsvConverter(image, dirname, imageID):

    hsvImage = image
    cv2.cvtColor(image, cv2.COLOR_BGR2HSV, hsvImage, 3 )

    h = hsvImage[: , : , 0]
    s = hsvImage[: , : , 1]
    v = hsvImage[: , : , 2]

    if not os.path.exists(dirname):
        os.mkdir(dirname)

    # cv2.imwrite(os.path.join(dirname, imageID+ "hsv.jpg"), hsvImage)
    # cv2.imwrite(os.path.join(dirname, imageID+ " h channel.jpg"), h)
    # cv2.imwrite(os.path.join(dirname, imageID + " s channel.jpg"), s)
    # cv2.imwrite(os.path.join(dirname, imageID + " v channel.jpg"), v)

    return hsvImage,h, s, v



def erosion(image):

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))

    # array([[0, 0, 1, 0, 0],
    #        [1, 1, 1, 1, 1],
    #        [1, 1, 1, 1, 1],
    #        [1, 1, 1, 1, 1],
    #        [0, 0, 1, 0, 0]], dtype = uint8)


    opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

    return opening


# take the eye area
def cut_eye_pos(in_img):


    out = in_img.copy()

    in_height = in_img.shape[0]
    in_width = in_img.shape[1]

    # number of rows to be cut from each side
    n_rows = math.floor(in_height * H_RATIO)
    # number of collumns to be cut from each side
    n_col_right = math.floor(in_width * W_RATIO)
    n_col_left = math.floor(in_width * (W_RATIO+0.18))


    # start and end indexes
    xs = n_rows
    xe = in_height - n_rows
    ys = n_col_left
    ye = in_width - n_col_right

    return out[xs:xe,ys:ye]



k = 1

current_folder = os.getcwd()

imageNames = []


for i in range(1,N_IMAGES+1):

    number = str(i)

    image_name = current_folder+"/source_images/videoCapTest/"+ number + ".jpg"
    imageNames.append(image_name)
    print(image_name)

for name in imageNames:

    fileNumber = str(k)
    k += 1

    orig_img = cv2.imread(name)
    eye = cut_eye_pos(orig_img)

    resultEqualization = createClare(eye)

    #hsv results

    #imageHSV, H, S, V = hsvConverter(eye, current_folder, fileNumber)



    channel = resultEqualization[:,:,2]
    img_gray = cv2.cvtColor(eye, cv2.COLOR_BGR2GRAY)


    imgScale = np.float32(img_gray)/255.0
    imageResult = imgScale
    dst = cv2.dct(imgScale)
    img = np.uint8(dst) * 255


    # channel = resultEqualization[:,:,0]


    img = cv2.medianBlur(channel, 5)

    ret, img = cv2.threshold(img, 45, 255, cv2.THRESH_BINARY)
    #36

    #imageEroded = erosion(img)

    #cv2.imwrite(os.path.join(dirnameErosion, fileNumber + ".jpg"), imageEroded)


    print("funky path :", current_folder)

    print("file name ", fileNumber)




    dirname = current_folder + "/results"

    cv2.imwrite(os.path.join(dirname,fileNumber + ".jpg"), img)

    