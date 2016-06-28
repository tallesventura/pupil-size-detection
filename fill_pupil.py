#!/usr/env python

import cv2
import numpy as np
import math


def fill_object(image, center, threshold):

    pixels = [center]
    img_row, img_col = image.shape
    bw_image = np.zeros(image.shape, np.uint8)
    for pxl in pixels:
        row, col = pxl

        if (row+1 < img_row) and (col+1 < img_col) and (row > 1) and (col > 1):
            neighborhood = [(row, col-1), (row-1, col), (row, col+1), (row+1, col)]
            for n in neighborhood:
                if image[n] <= threshold:
                    bw_image.itemset(pxl, 255)
                    image.itemset(n, 41)
                    pixels.append(n)
        else:
            break

    img2, contours, hierarchy = cv2.findContours(bw_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if contours and len(contours[0]) > 5:
        cnt = contours[0]
        ellipse = cv2.fitEllipse(cnt)
        print(ellipse)
        cv2.ellipse(image, ellipse, 255, 2)
    # cv2.imshow("r", img2)
    # cv2.waitKey(0)
    # print(maxi, mini)
    size = 0
    return image, size


# img is a binary preprocessed image
def rough_pupil_point(img):

    VARIANCE = 55
    img_inverted = cv2.bitwise_not(img)
    row, col = img_inverted.shape
    gaussian_x = cv2.getGaussianKernel(row, VARIANCE)
    gaussian_y = cv2.getGaussianKernel(col, VARIANCE)
    gaussian_weight = gaussian_x * np.transpose(gaussian_y)
    weighted_image = np.multiply(img_inverted, gaussian_weight)
    rough_point = np.unravel_index(weighted_image.argmax(), weighted_image.shape)
    return rough_point


def resolution_normalization(image):
    normalized = cv2.resize(image, (1344, 756), interpolation=cv2.INTER_LINEAR)
    return normalized


def nan_cleaning(float_list):
    cleaned_data = []
    for value in float_list:
        if not math.isnan(value):
            cleaned_data.append(value)
    return cleaned_data


if __name__ == '__main__':

    import os
    threshold = 40
    folder = "source_images/results/"
    files = [x for x in os.listdir(folder) if os.path.isfile(os.path.join(folder, x))]
    files.sort()
    size_list = []
    for i in range(0, len(files), 2):

        # print(files[i])
        path = folder+files[i]
        path_original = folder+files[i+1]
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        center_point = rough_pupil_point(img)
        img_original = cv2.imread(path_original, cv2.IMREAD_GRAYSCALE)
        filled_image, size = fill_object(img_original, center_point, threshold)
        if size > 0 :
            size_list.append(size)
        # print(size)
        # cv2.imshow("pupil", filled_image)
        # cv2.waitKey(0) & 0xff
        l = files[i].split('.')
        result_name = l[0]+"_filled.jpg"
        current_folder = os.getcwd()
        result_path = "source_images/fill-pupil"
        cv2.imwrite(os.path.join(result_path,result_name), filled_image)

    import matplotlib.pyplot as plt
    plt.plot(size_list)
    plt.ylabel("size in pixels")
    plt.show()
