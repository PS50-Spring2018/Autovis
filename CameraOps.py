
import time
import cv2
import numpy as np

def stream(n=0):

    """ 
    Functionality 
    ---------------------------------------------------------
    streams webcam to a window

    Vars
    ---------------------------------------------------------
    n       |   number used to ID camera to be used
   
    Returns
    ---------------------------------------------------------
       
    """

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
    

def snap(n=0):

    """ 
    Functionality 
    ---------------------------------------------------------
    snaps an instant of the webcam and displays

    Vars
    ---------------------------------------------------------
    n       |   number used to ID camera to be used
   
    Returns
    ---------------------------------------------------------
       
    """
    vc = cv2.VideoCapture(n)
    if vc.isOpened(): # try to get the first frame
        
        #key = cv2.waitKey(50)

        rval, frame = vc.read()
        cv2.imwrite("frame%d.jpg" % n, frame) #save the image as jpg 

    else:
        rval = False
        frame = None

    vc.release()
    return frame


def detect(self, initial_img):

    """ 
    Functionality 
    ---------------------------------------------------------
    thresholds image from webcam, fits contours

    Vars
    ---------------------------------------------------------
    initial_img |   Inputted image from the webcam 
   
    Returns
    ---------------------------------------------------------
    center[ind] |   the center of the largest circle detected
    radii[ind]  |   the radiius of the largest circle detected    
    """
    
    gray = cv2.cvtColor(initial_img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY_INV)[1]
    
    _, cont,hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) #finds contours
    
    center=[]
    radii=[]

    for line in cont:
        temp=circle(line)
        center.append(temp[0])
        radii.append(temp[1])
    
    radii=np.array(radii)
    ind=np.argmax(radii) #gets index of largest circle detected

    return center[ind],radii[ind]


def circle(cnt):  

    """ 
    Functionality 
    ---------------------------------------------------------
    fits contour to a circle

    Vars
    ---------------------------------------------------------
    cnt         |   inputted contour

    Returns
    ---------------------------------------------------------
    center      |   the center of the largest circle detected
    radii       |   the radiius of the largest circle detected    
    """ 

    (x,y),radius = cv2.minEnclosingCircle(cnt) 
    center = (int(x),int(y))
    radius = int(radius)

    return center, radius 
