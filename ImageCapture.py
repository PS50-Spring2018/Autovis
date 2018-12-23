
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
		self.reaction_id=rxn_id
		self.interv = interv
		self.t = time
		self.dir_file = dir_file
		self.rxn_foldername = os.path.join(self.dir_file, str(self.reaction_id))
		self.n = n

	def run_image(self):
		'''
		Creates the reaction directory, if it does not already exists, and starts the process to take images
		for the set amount of time and iterations. 
		'''
		if not os.path.exists(self.rxn_foldername):
			os.makedirs(self.rxn_foldername) #makes a reaction directory

		for i in range(int(self.t/self.interv)): 
			tempM,tempV=self.iteration() #runs a single image process
			time.sleep(self.interv) #time intervals between trials
			
			#currentDT = datetime.datetime.now() #gets the current date and time
			#time=currentDT.strftime('%Y%m%d%H%M%s') #formats the time 

	def getTime(self):
		'''
		Gets the current time and saves it as an unique string
		Returns: 
			time: string | The time formatted YearMonthDayHourMinuteSecond, Ex: 20180721065911
		
		'''
		currentDT = datetime.datetime.now() #gets the current date and time
		time=currentDT.strftime('%Y%m%d%H%M%s') #formats the time 
		#time="filler"
		#time=str(uuid.uuid4())#for PCs/santi's computer

		
		
		return time
	


	def ObtainImage(self):
		'''
		Captures a single image, locally save the image, detects a beaker, and calculates color statistics
		Returns: 
			mean: array | Mean of the RGB colors in the image
			var: array  | Variance of the RGB colors in the image
		'''
		initial_img = co.snap(self.n) 
		name= self.getTime() #write raw image to a file
		direct=os.getcwd()

		cv2.imwrite("%sframe%s.jpg" % (direct,name), initial_img)  #reads back that image in the correct format
		img = cv2.imread("%sframe%s.jpg" % (direct,name)) 
		

		#reads in image to cv2 for shape detecting
		#img = img[:,:,::-1] # Change BGR to RGB format - Tim - Testing
		#print('***img',img[:2,:2,:])
		#detects the beaker location and size, adjusts size
		#cv2.imshow('image',img)
		#cv2.waitKey(0)
		#cv2.destroyAllWindows()

		center, radius = co.detect(self,img)
		radius = radius - int(0.1*radius)

		return name, img, center, radius

	def iteration(self):
		name, img, center, radius = self.ObtainImage()

		# Draw circle into image
		#img = img[:,:,::-1]
		circle=cv2.circle(img,center,radius,(0,255,0),2)
		circle = circle[:,:,::-1] #Change BGR to RGB format - Tim
 		#Change BGR to RGB format - Tim
		np.save(self.rxn_foldername+"/%s.npy" % (name),circle)

		mask=np.zeros((int(img.shape[0]),int(img.shape[1]),3))

		
		#cv2.imshow("image",circle)
		#cv2.waitKey(0)
		#cv2.destroyAllWindows()
		#Sets the extreme bounds of the circle
		#this is used to detect boundaries and ensure that there is no out of bounds exceptions
		#this creates a mask to not include values outside of the circle 
		

		down=min(img.shape[0],center[1]+radius)
		up=max(center[1]-radius,0)

		
		#print(up, down)
		for i in np.arange(up,down):
			#print(i)

			deltax=int(np.sqrt(np.abs(int(radius)**2-int(i-center[1])**2)))
			#deltax=int(np.sqrt(np.abs(int(radius)**2-int(i-center[1])**2)))

			left=center[0]-deltax
			right=center[0]+deltax
			#print("y: " + str(i) + " left: " + str(max(left,0)) + " right: "+ str(min(right,int(img.shape[0]))))
			left=max(left,0)
			right=min(right,int(img.shape[1]))
			x=np.arange(left,right)
			mask[i,x,:]=1

			
		#Applies mask


		img_masked = np.multiply(img, mask)
		#cv2.imshow("mask",img_masked)
		#cv2.waitKey(0)
		#cv2.destroyAllWindows()


		img_nonzero = []
		
		# Goes through image and appends pixels that are in circle
		for row in range(mask.shape[0]):
			for col in range(mask.shape[1]):
				#Detects where in the mask nan values are present sorts it
				if int(mask[row,col,:].any()) == 1:
					img_nonzero.append(img[row, col])

		img_nonzero = np.array(img_nonzero)
	
		
		mean=[np.mean(img_nonzero[:,0]),np.mean(img_nonzero[:,1]),np.mean(img_nonzero[:,2])]
		var=[np.std(img_nonzero[:,0]),np.std(img_nonzero[:,1]),np.std(img_nonzero[:,2])]

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

