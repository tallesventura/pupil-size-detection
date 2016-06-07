#! /usr/env python

import numpy as np
import cv2
import os
from matplotlib import pyplot as plt


def createClare(img):

    #get path

    image = img

    channelB = image[: , :, 0]
    channelG = image[: , :, 1]
    channelR = image[: , :, 2]

    # create a CLAHE object(Contrast Limited Adaptive Histogram Equalization)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(5, 5))
    cl1 = clahe.apply(channelB)
  #  cv2.imwrite('bluechannel.jpg', cl1)

    clahe1 = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(5, 5))
    cl2 = clahe1.apply(channelG)

   # cv2.imwrite(imageID, cl2)

    clahe2 = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(5, 5))
    cl3 = clahe2.apply(channelR)
    #cv2.imwrite('redChannel.jpg', cl3)

    result = cv2.merge((cl1, cl2, cl3))

    cv2.imwrite("channelb.jpeg", cl1)
    cv2.imwrite("channelg.jpeg", cl2)
    cv2.imwrite("channelr.jpeg", cl3)

    cv2.imwrite("result.jpeg", result)

    return result

current_folder = os.getcwd()

imageNames = []


for i in range(1,36):
    number = str(i)

    image_name = current_folder+"\\source_images" + "\\"+ number + ".jpg"
    imageNames.append(image_name)
    print(image_name)

for name in imageNames:

    eye = cv2.imread(name)
    resultEqualization = createClare(eye)

    channel = resultEqualization[:,:,0]

    # img = cv2.GaussianBlur(img, (5, 5), 10)

    # resultEqualization = createClare(eye)
    #
    # channel = resultEqualization[:,:,0]

    img = cv2.medianBlur(channel, 5)

    ret, th1 = cv2.threshold(img, 41, 255, cv2.THRESH_BINARY)

    # th2 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 3)
    #
    # th3 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 9, 3)
    #
    # titles = ['Original Image', 'Global Thresholding (v = 127)', 'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']
    #
    # images = [img, th1, th2, th3]

    cv2.imwrite(name, th1)

    # cv2.imwrite("afterthreshold.jpg",th1)


    # for i in range(4):
    #     plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
    #     plt.title(titles[i])
    #     plt.xticks([]),plt.yticks([])
    #     plt.show()