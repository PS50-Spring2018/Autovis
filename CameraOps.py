
import time
import cv2
import numpy as np

def stream(n=0):

    cv2.namedWindow("preview")
    
    vc = cv2.VideoCapture(n)

    if vc.isOpened(): # try to get the first frame
    
        rval, frame = vc.read()
    
        print('frame\n', frame[0][:])
    
    else:
    
        rval = False
    
        frame = None

    while rval:
    
        cv2.imshow("preview", frame)
    
        rval, frame = vc.read()
    
        if key == 27: # exit on ESC
    
            break

    cv2.destroyWindow("preview")
    vc.release()
    
# Function taking a single picture from webcam and returning it in array form
# n: Camera number on computer (usually n=0 for built-in webcam)
def snap(n=0):
    vc = cv2.VideoCapture(n)
    
    if vc.isOpened(): # try to get the first frame
        
        #key = cv2.waitKey(50)

        rval, frame = vc.read()
        #was added to save the image as 
        cv2.imwrite("frame%d.jpg" % n, frame) 

    else:
        rval = False
        frame = None

    vc.release()

    return frame