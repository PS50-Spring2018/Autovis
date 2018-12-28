""" Class for  communication with acquisition, data analysis and output """
import os
import sys
import time
import glob
import csv
import numpy as np
import cv2
from Dashboard import dashboard


class CommunicationManager(object):
    '''
    Class for communication with acquisition analysis and output.

    Parameters:
            dir_file: string      | Directory containing image data
            rxd_id: string or int | Reaction ID
    '''

    def __init__(self, dir_file, rxn_id):
        '''
        Initializes the CommunicationManager class.
        '''
        self.dir_file = dir_file
        self.reaction_id = rxn_id

        self.csvname = 'summary_{}.csv'.format(rxn_id)  # name of file
        self.processed_indices = [0]  # list of image indices processed
        self.means = []  # list of RGB means
        self.variances = []  # list of RGB variances

    def initialize(self):
        '''
        Change to image directory.
        '''
        path_data = os.path.join(self.dir_file, self.reaction_id)
        os.chdir(path_data)

    def run(self):
        '''
        Runs analysis loop:  checks for new images, loads, and plots dashboard.
        Exit analysis loop with ctrl-c.
        '''

        # Structure to exit analysis loop with ctrl-c
        try:
            # Continuously check for new images
            while True:

                # Try loading data and plotting dashboard
                try:
                    # Load data from current image
                    mean_array, var_array, im_arr = self.load_data()

                    # Append to mean and variance list for all images
                    self.means.append(mean_array)
                    self.variances.append(var_array)

                    # Plot dashboard
                    dashboard(np.array(self.means), np.array(self.variances), im_arr)

                    # Update which images have been processes
                    self.processed_indices.append(self.processed_indices[-1]+1)

                    # Pause to wait for new images to be collected
                    time.sleep(2.)

                # If we ran out of images: pause to wait for new images
                except IndexError:
                    print('Waiting for new images...')
                    time.sleep(5)

        except KeyboardInterrupt:
            print('\nCommunicationManager closed by user')
            pass

    def load_data(self):
        '''
        Loads data from image and summary files.

        Returns:
            mean_array: array  | RGB value means of current image
            var_array: array   | RGB value variances of current image
            im_arr: array | Current image in array format
        '''

        # Get current time stamps
        timestamps = self.gettimestamp()

        # Load the next image
        last_img_index = self.processed_indices[-1]
        im_arr = np.load('{}.npy'.format(timestamps[last_img_index]))

        # Load data from summary csv file

        with open(self.csvname, 'r') as csvfile:
            reader = csv.reader(csvfile)
            my_csv_data = list(reader)
        # grabs the mean & variance data of the current image
        data = my_csv_data[last_img_index]

        # Create arrays of RGB value means and variances
        mean_array = [float(data[1]), float(data[2]), float(data[3])]
        var_array = [float(data[4]), float(data[5]), float(data[6])]

        return mean_array, var_array, im_arr

    def gettimestamp(self):
        '''
        Creates list of timestamps of files in the directory.
        '''
        timestamps = []

        # for every .npy file in the current directory
        for file in glob.glob("*.npy"):
            name = file.split('.')
            # grab the timestamp portion
            timestamp_str = name[0]
            # convert the timestamp string into an integer
            timestamp_int = int(timestamp_str)
            # append to list of timestamps
            timestamps.append(timestamp_int)

        # sorts the timestamps in increasing order
        timestamps.sort()

        return timestamps
