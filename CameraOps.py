
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

"""
Functionality: 

Variables:
    -gray: converts image to a grey image
    -blur: blurs image
    -thresh: performs thresholding on image
    -cont: contours of findcontour 
    -hierarchy: number of contour detected
"""
def detect(self, initial_img):
    # initialize the shape name and approximate the contour
    #image preprocessing
    gray = cv2.cvtColor(initial_img, cv2.COLOR_BGR2GRAY)
    
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    
    thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY_INV)[1]
    #finds contours
    _, cont,hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    
    center=[]
    radii=[]

    for line in cont:

        temp=circle(line)
        
        center.append(temp[0])
        
        radii.append(temp[1])
    
    radii=np.array(radii)
    #gets biggest circle
    ind=np.argmax(radii)

    return center[ind],radii[ind]
"""
funtionality: returns the radius and center of the minimum enclosing circle
"""

def circle(cnt):   
    #fits contour to a circle
    (x,y),radius = cv2.minEnclosingCircle(cnt)

    center = (int(x),int(y))

    radius = int(radius)

    return center, radius 
