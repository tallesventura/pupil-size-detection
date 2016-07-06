#!/usr/env python

import os
import cv2


# given a function a its arguments apply it to all images of a given folder and create a new folder with the result
def folder_operation(function, *args, folder='source_images', local=False):

    if local == True:
        local_folder = os.getcwd()
        folder_operation(function, args, folder=local_folder)

    else:
        files = [x for x in os.listdir(folder) if os.path.isfile(os.path.join(folder, x))]
        new_folder = folder+"/"+function.__name__

        if not os.path.exists(new_folder):
            os.mkdir(new_folder)

        for file in files:
            file = folder+"/"+file
            img = cv2.imread(file)
            list_args = list(args)
            list_args.insert(0,img)
            args = tuple(list_args)
            result = function(*args)
            cv2.imwrite(new_folder+'/'+file, result)
            list_args = list(args)
            list_args.pop(0)
            args = tuple(list_args)


if __name__ == "__main__":
    from fill_pupil import resolution_normalization
    folder_operation(resolution_normalization)