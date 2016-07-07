#! /usr/env python

import numpy as np
import cv2
import math
import os


# height shrinkage ratio
H_RATIO = 0.13
# width shrinkage ratio
W_RATIO = 0.1


def createClare(img):

    image = img

    channelB = image[: , :, 0]
    channelG = image[: , :, 1]
    channelR = image[: , :, 2]

    # create a CLAHE object(Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cl1 = clahe.apply(channelB)

    clahe1 = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cl2 = clahe1.apply(channelG)

    clahe2 = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cl3 = clahe2.apply(channelR)

    result = cv2.merge((cl1, cl2, cl3))

    return result


def erosion(image):

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
    opening = cv2.morphologyEx(image, cv2.MORPH_DILATE, kernel)

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


def run(image_names, src_path, gray_path, binarized_path):

    for name in image_names:
        orig_img = cv2.imread(src_path + "/" + str(name) + ".jpg")
        eye = cut_eye_pos(orig_img)
        resultEqualization = createClare(eye)
        img_gray = cv2.cvtColor(resultEqualization, cv2.COLOR_BGR2GRAY)
        blured_img = cv2.GaussianBlur(img_gray, (5, 5), 10)
        ret, bin_img = cv2.threshold(blured_img, 39, 255, cv2.THRESH_BINARY)

        for i in range(4):
            bin_img = erosion(bin_img)

        cv2.imwrite(gray_path + "/" + str(name) + ".jpg", blured_img)
        cv2.imwrite(binarized_path + "/" + str(name) + ".jpg", bin_img)

 