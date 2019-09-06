""" Class for taking webcam images and storing image statistics """

import time
import cv2
import numpy as np
import CameraOps as co
import csv as csv
import os
import datetime
import uuid
from matplotlib import pyplot as plt


class ImageCapture:
    """
    ImageCapture is the class the contains the functions required to take images and
    to identify shapes in the images.
    Parameters:
        rxn_id:         string  | Reaction identifier.
        interv:         float   | Time between pictures being taken.
        t:              float   | Total time of the experiment.
        dir_file:       string  | The path of new picture files.
        n:              int     | camera number, 0 for built in, 1 for external

    Notes:
    """
    def __init__(self, time, interv, rxn_id, dir_file, n):
        self.rxn_id = rxn_id
        self.interv = interv
        self.t = time
        self.dir_file = dir_file
        self.rxn_foldername = os.path.join(dir_file, str(rxn_id))
        self.n = n

    def run(self):
        '''
        Creates the reaction directory, if it does not exist, and takes images
        for the set amount of time and iterations.
        '''
        if not os.path.exists(self.rxn_foldername):

            os.makedirs(self.rxn_foldername)  # makes a reaction directory

        for i in range(int(self.t/self.interv)):
            tempM, tempV = self.iteration()  # runs a single image process
            time.sleep(self.interv)  # time intervals between trials

    def getTime(self):
        '''
        Gets the current time and saves it as an unique string

        Returns:
        time: string | The time formatted YearMonthDayHourMinuteSecond
        '''

        currentDT = datetime.datetime.now()  # gets the current date and time
        time = currentDT.strftime("%Y%m%d%H%M%S")  # formats the time
        #time=str(uuid.uuid4())#for PCs/santi's computer
        return time

    def ObtainImage(self):
        '''
        Captures a single image, saves it, detects beaker, and calculates stats

        Returns:

        mean: array | Mean of the RGB colors in the image
        var: array  | Variance of the RGB colors in the image
        '''
        initial_img = co.snap(self.n)
        name = self.getTime()  # write raw image to a file
        direct = os.getcwd()
        # reads back that image in the correct format
        cv2.imwrite('%sframe%s.jpg' % (direct, name), initial_img)
        img = plt.imread('%sframe%s.jpg' % (direct, name))

        center, radius = co.detect(img)
        radius = radius - int(0.1*radius)

        return name, img, center, radius

    def iteration(self):
        name, img, center, radius = self.ObtainImage()
        # Draw circle into image
        circle = cv2.circle(img, center, radius, (0, 255, 0), 2)
        circle = circle[:, :, ::-1]  # Change BGR to RGB format
        np.save(self.rxn_foldername+"/%s.npy" % (name), circle)
        mask = np.zeros((int(img.shape[0]), int(img.shape[1]), 3))
        # Sets the extreme bounds of the circle
        # this detects boundaries and ensures that there is no out of bounds
        # this creates a mask to not include values outside of the circle
        down = min(img.shape[0], center[1]+radius)
        up = max(center[1]-radius, 0)

        for i in np.arange(up, down):
            deltax = int(np.sqrt(np.abs(int(radius)**2-int(i-center[1])**2)))
            left = center[0]-deltax
            right = center[0]+deltax
            left = max(left, 0)
            right = min(right, int(img.shape[1]))
            x = np.arange(left, right)
            mask[i, x, :] = 1
        # Applies mask
        img_masked = np.multiply(img, mask)
        img_nonzero = []
        # Goes through image and appends pixels that are in circle
        for row in range(mask.shape[0]):
            for col in range(mask.shape[1]):
                # Detects where in the mask nan values are present sorts it
                if int(mask[row, col, :].any()) == 1:
                    img_nonzero.append(img[row, col])

        img_nonzero = np.array(img_nonzero)
        mean = [np.mean(img_nonzero[:, 0]), np.mean(img_nonzero[:, 1]), np.mean(img_nonzero[:, 2])]
        var = [np.std(img_nonzero[:, 0]), np.std(img_nonzero[:, 1]), np.std(img_nonzero[:, 2])]
        
        # file to save the output of the program
        folder = self.rxn_foldername

        with open(folder+'/summary_%s.csv' % (self.rxn_id), 'a+') as csvfile:
            swriter = csv.writer(csvfile)
            swriter.writerow([name, mean[2], mean[1], mean[0], var[2], var[1], var[0]])

        return mean, var

