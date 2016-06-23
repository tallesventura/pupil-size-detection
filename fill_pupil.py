#!/usr/env python

import cv2
import numpy as np
import math

def fill_object(image, center, threshold):
    pixels = [center]
    img_row, img_col = image.shape
    mini = center[0]
    maxi = center[0]

    for pxl in pixels:
        row, col = pxl

        if row > maxi:
            maxi = row
        elif row < mini:
            mini = row

        if (row+1 < img_row) and (col+1 < img_col) and (row > 1) and (col > 1):
            neighborhood = [(row, col-1), (row-1, col), (row, col+1), (row+1, col)]
            for n in neighborhood:
                if image[n] <= threshold:
                    pixels.append(n)
                    image[n] = 255
        else:
            break

    diameter = maxi - mini
    #print(maxi, mini)
    return image, diameter


# img is a binary preprocessed image
def rough_pupil_point(img):

    VARIANCE = 55
    img_inverted =  cv2.bitwise_not(img)
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


if __name__ == '__main__':

    # path = 'source_images/2.jpg'
    # img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    # img = cv2.resize(img, None, fx=0.2, fy=0.2, interpolation=cv2.INTER_LINEAR)
    # threshold = 60
    # center = (115,210)
    # img2, size = fill_object(img, center, threshold)
    # cv2.imshow("test", img2)
    # cv2.waitKey(0) & 0xff
    # print(size)
    #
    # img_equalized = cv2.imread('source_images/equalized.jpg', cv2.IMREAD_GRAYSCALE)
    # img_equalized = cv2.resize(img_equalized, None, fx=0.3, fy=0.3, interpolation=cv2.INTER_LINEAR)
    # point = rough_pupil_point(img_equalized)
    # print(point)
    # cv2.imshow("test", img_equalized)
    # cv2.waitKey(0) & 0xff
    import os
    threshold = 40
    folder = "source_images/results/"
    files = [x for x in os.listdir(folder) if os.path.isfile(os.path.join(folder, x))]
    files.sort()
    for i in range(0,len(files),2):

        print(files[i])
        path = folder+files[i]
        path_original = folder+files[i+1]
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        center_point = rough_pupil_point(img)
        img_original = cv2.imread(path_original, cv2.IMREAD_GRAYSCALE)
        filled_image, size = fill_object(img_original, center_point, threshold)
        #print(size)
        # cv2.imshow("pupil", filled_image)
        # cv2.waitKey(0) & 0xff
        l = files[i].split('.')
        result_name = l[0]+"_filled.jpg"
        current_folder = os.getcwd()
        result_path = "source_images/fill-pupil"
        cv2.imwrite(os.path.join(result_path,result_name), filled_image)





