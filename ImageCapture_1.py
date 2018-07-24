
import time
import cv2
import numpy as np
import CameraOps as co
import csv as csv
import os
import datetime
from matplotlib import pyplot as plt

class ImageCapture:
    """
    ImageCapture is the class the contains of all of the functions required to gather images and 
    to identify shapes in the images. 

    Parameters: 
        reaction_id:    string  | Reaction identifier. 
        interv:         float   | Time between pictures being taken.
        t:              float   | Total time of the experiment.
        dir_file:       string  | The path of the destination of the picture files.
        n:              int     | The camera number, usually 0 for built in camera and 1 for webcam.
       
    Notes:

    """
	def __init__(self, time, interv,rxn_id, dir_file, n):
        '''
        Initializes the ImageCapture class.
        '''
		self.reaction_id=rxn_id
		self.interv=interv
		self.t  = time
		self.dir_file = dir_file
		self.rxn_foldername = os.path.join(self.dir_file, str(self.reaction_id))
        self.n = n

	def run(self):
        '''
        Creates the reaction directory, if it does not already exists, and starts the process to take images
        for the set amount of time and iterations. 
        '''
		if not os.path.exists(self.rxn_foldername):
			os.makedirs(self.rxn_foldername) #makes a reaction directory

		for i in range(int(self.t/self.interv)): 
			tempM,tempV=self.iteration() #runs a single image process
			time.sleep(self.interv) #time intervals between trials
			
	def getTime(self):
		'''
        Gets the current time and saves it as an unique string

        Returns: 
            time: string | The time formatted YearMonthDayHourMinuteSecond, Ex: 20180721065911
        '''
		currentDT = datetime.datetime.now() #gets the current date and time
		time=currentDT.strftime('%Y%m%d%H%M%s') #formats the time 

		return time
    '''
    FIRST COPY OF ITERATION
    '''
		
	def iteration(self):
		'''
        Captures a single image, locally save the image, detects a beaker, and calculates color statistics

        Returns: 
            mean: array | Mean of the RGB colors in the image
            var: array  | Variance of the RGB colors in the image

        '''
		initial_img = co.snap(self.n) #Gets raw image
		name= self.getTime() #Gets the name for the image
		cv2.imwrite("frame%s.jpg" % name, initial_img) #Writes raw image to file
		img = cv2.imread("frame%s.jpg" % name) #Reads in image to cv2 for shape/color detecting

		#img = img[:,:,::-1] # Change BGR to RGB format - Tim
		print('***img',img[:2,:2,:])
		center, radius = co.detect(co, img) #Detects center and radius of beaker
		radius = radius - int(0.1*radius)

		# Draw circle into image
		circle=cv2.circle(img,center,radius,(0,255,0),2)
		circle = circle[:,:,::-1] #Change BGR to RGB format - Tim
		np.save(self.rxn_foldername+"/%s.npy" % (name),circle)
		img = img[:,:,::-1] #Change BGR to RGB format - Tim

		mask=np.zeros((int(img.shape[0]),int(img.shape[1]),3))
	   
       #Sets extreme values
		left=radius
		right=radius
		top=radius
		bottom=radius

		for i in range(int(radius)):
			delta=int(np.sqrt(int(radius)**2-int(i)**2))
			
			left=delta
			right=delta
			up=i
			down=i
			#this is used to detect boundaries and ensure that there is no boudary jumping
			if mask.shape[0]<center[0]+right:
				right=-center[0]+mask.shape[0]-1
			if 0>center[0]-left:
				left=center[0]
			if mask.shape[1]<center[1]+down:
				down=-center[1]+mask.shape[1]-1
			if 0>center[1]-up:
				up=center[1]
			
			#pythagorean
			delta=int(np.sqrt(int(radius)**2-int(i)**2))
			x=np.arange(int(center[0])-left,int(center[0])+right)
			mask[x,(center[1]-up),:] = np.nan
			mask[x,(center[1]+down),:] = np.nan
		
		# # Applies mask
		# img_masked = img * mask

		mask = np.array(mask)
		img_nonzero = []

		# Goes through image and appends pixels that are in circle
		for row in range(mask.shape[0]):
			for col in range(mask.shape[1]):
				if not np.isnan(mask[row, col]).all():
					img_nonzero.append(img[row, col])

		img_nonzero = np.array(img_nonzero)

		print('***shape of image:', img.shape)
		print('***shape of img_nonzero:', img_nonzero.shape)

		# # Goes through image and appends pixels that are in circle...TESTING
		# img_nonzero = []
		# for i in range(img.shape[0]):
		#     for j in range(img.shape[1]):
		#         if not all(img_masked[i,j]==[0,0,0]):
		#             img_nonzero.append(img_masked[i,j])
		# img_nonzero = np.array(img_nonzero)

		print('****************')
		print('img_nonzero', img_nonzero)

		mean=[np.mean(img_nonzero[:,0]), np.mean(img_nonzero[:,1]), np.mean(img_nonzero[:,2])]
		var=[np.std(img_nonzero[:,0]), np.std(img_nonzero[:,1]), np.std(i_nonzero[:,2])]
		
		# file to save the output of the program
		self.save(self.reaction_id,name,mean,var,self.rxn_foldername)
		return mean, var
   

    
    def save(self,rxnID, file, mean, variance, folderwoID):
    '''
    Saves csv file and writes statistics to it. 

    Parameters: 
        rxnID: float/string | The reaction identifier. 
        file: string        | File name of the image being added to the csv
        mean: array         | Mean of the RGB values in the image. 
        variance: array     | Variance of the RGB values. 
        folderwoID:  string | The file path to the directory where images are being saved. 
    '''
        with open(folderwoID+'/summary_%s.csv' % (rxnID),'a+') as csvfile:
            swriter = csv.writer(csvfile)
            swriter.writerow([file, mean[0],mean[1],mean[2], variance[0],variance[1],variance[2]])
