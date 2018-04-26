import os # operating systmem interface
import glob # accesses the global directory
import numpy as np # work with arrays, list, list images as arrays, etc.
import csv # read the csv file
import time # later call the kernel to sleep using time.sleep
import sys
#sys.path.append('/Users/nicolekim/Desktop/PS50/repo/DataAnalysis')
sys.path.append('../DataAnalysis')
from dashboard_function import dashboard # Data Analysis dashboard plot function


# CHANGE TO DROPBOX DIRECTORY
path = '/Users/tim/Google Drive/Teaching/'

def getdropbox():
	"""Checks dropbox and updates list of timestamps as integers.
	Note: Assumes we're inside the dropbox directory.

	Returns:
	========
	lst_of_TS : list of timestamps (as integers not filenames)
	"""
	lst_of_TS = [] # initiate list of all the timestamps of the files for keeping track of updates

	for file in glob.glob("*.npy"): # "for every .npy file in the current directory "

		name = file.split('.') # split file name into list of 2 string elements, "timestamp" + ".npy"
		timestamp_str = name[0] # grab the timestamp portion 
		timestamp_int = int(timestamp_str) # convert the timestamp string into an integer
		lst_of_TS.append(timestamp_int) # append to list of timestamps

	lst_of_TS.sort() # sorts the list of timestamps in increasing order
	return lst_of_TS


## Running script 
""" Asks user for reaction ID (corresponds to input to Webcam Interface)
	Changes working directory to the dropbox 
	initializes variables of means and variances 
	While loop is for continuous checking of the dropbox for new images
"""
reaction_id= input("What is the reaction ID?") # by default, user input is a string

path = path + reaction_id

dirpath = os.getcwd()
print("Current working directory %s" % dirpath)

os.chdir(path)
# Check current working directory.
dirpath = os.getcwd()

print("Directory changed successfully %s" % dirpath) 

csvname = str('summary_' +  reaction_id + ".csv")
csvpath = os.path.join(dirpath, csvname) # create path to access csv for specific reaction
lst_current_indices = [0] # list of indices that have been worked with/sent to Data Analysis team
means = [] # list of R,G,B means
variances = [] # list of R,G,B variances


i = 0
while i==0:
	# dashboard() - initialize dashboard
	lst_of_TS = getdropbox() 
	
	last_img_index = lst_current_indices[-1] # obtain the last image file that hasn't been worked with already
	image_array = np.load(str(lst_of_TS[last_img_index])+ '.npy') # numpy array for image data

	csvfile = open(csvpath, 'r')
	reader = csv.reader(csvfile)
	my_csv_data = list(reader) 
	rawdata = my_csv_data[last_img_index] # grabs the mean & variance data of the current image
	csvfile.close()

	data = rawdata 
	mean_array = [float(data[1]), float(data[2]), float(data[3])] # create array of mean RGB values
	var_array = [float(data[4]), float(data[5]), float(data[6])]  # create array of variance of RGB values
	# Format data for Data Analysis dashboard function 
	means.append(mean_array)
	variances.append(var_array)

	means_temp = np.array(means)
	#means_temp = np.array([[94, 110, 2]]) #for testing
	variances_temp = np.array(variances)

	print('means_temp:', means_temp)
	dashboard(means_temp, variances_temp, image_array) #plot the information on the dashboard

	 
	lst_current_indices.append(last_img_index+1) # increment index by 1


	# Data analysis plot function(output) updates the dashboard
	time.sleep(0.5)

	#exit()

	# Testing by Tim - JUST PAUSES PROCESSOR FOR 20s
	time.sleep(20)
	break
