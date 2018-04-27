
import time
import cv2
import numpy as np
import CameraOps as co
import ShapeDetector as sd
import csvSave as csvSave
import os
import datetime

class Processor:
    
    def __init__(self, time, interv,rxn_id, dropbox_dir):
        
        self.reaction_id=rxn_id
    
        self.interv=interv

        self.t  = time
        
        self.dropbox_dir = dropbox_dir
        self.rxn_foldername = os.path.join(self.dropbox_dir, str(self.reaction_id))

    def run(self):
        

        #creates director for dropbox
        if not os.path.exists(self.rxn_foldername):
        
            os.makedirs(self.rxn_foldername)

        for i in range(int(self.t/self.interv)):
            #runs a single image process
            tempM,tempV=self.iteration()
            #time intervals between trials
            time.sleep(self.interv) 
            
            
    def getTime(self):
        #gets time
        currentDT = datetime.datetime.now()
        #formats
        time=currentDT.strftime('%Y%m%d%H%M%s')
        
        return time
    
    def iteration(self):

        #foldername = "/Users/shreyamenon/Dropbox/%s" % self.reaction_id
        #foldername = '/Users/tim/Google Drive/Teaching/%s' % (self.reaction_id)
        
        #change to 1 for functionality of the webcam
        initial_img = co.snap(0)

        #name = self.getTime()
        name= self.getTime()

        cv2.imwrite("frame%s.jpg" % name, initial_img)
        
        img = cv2.imread("frame%s.jpg" % name)

        center, radius = sd.detect(sd, img)

        circle=cv2.circle(img,center,radius,(0,255,0),2)
        np.save(self.rxn_foldername+"/%s.npy" % (name),circle)

        mask=np.zeros((int(img.shape[0]),int(img.shape[1]),3))
    
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
                    img_nonzero.append(mask[row, col])

        img_nonzero = np.array(img_nonzero)


        # # Goes through image and appends pixels that are in circle
        # img_nonzero = []
        # for i in range(img.shape[0]):
        #     for j in range(img.shape[1]):
        #         if not all(img_masked[i,j]==[0,0,0]):
        #             img_nonzero.append(img_masked[i,j])
        # img_nonzero = np.array(img_nonzero)

        print('****************')
        print('img_nonzero', img_nonzero)

        mean=[np.mean(img_nonzero[:,0]), np.mean(img_nonzero[:,1]), np.mean(img_nonzero[:,2])]
        
        var=[np.var(img_nonzero[:,0]), np.var(img_nonzero[:,1]), np.var(img_nonzero[:,2])]
        
        # file to save the output of the program
        csvSave.save(self.reaction_id,name,mean,var,self.rxn_foldername)

        return mean, var