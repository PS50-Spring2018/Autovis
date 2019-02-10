""" Utilities for image capture and processing derived from the OpenCV"""

import time
import cv2
import numpy as np



def snap(n=0):
    '''
    Snaps an instant of the webcam and displays

    Parameters:
        n: int       | Number used to ID camera to be used

    Returns:
        frame: array | Frame captured by webcam
    '''
    vc = cv2.VideoCapture(n)
    if vc.isOpened():  # try to get the first frame
        # key = cv2.waitKey(50)
        rval, frame = vc.read()
        # save the image as jpg
        cv2.imwrite("frame%d.jpg" % n, frame)

    else:
        rval = False
        frame = None

    vc.release()
    return frame


def detect(initial_img):
    '''
    Thresholds image from webcam and fits contours

    Parameters:
        initial_img: array | Inputted image from the webcam

    Returns:
        center[ind]: float | Center of the largest circle detected
        radii[ind]: float  | Radiius of the largest circle detected
    '''

    gray = cv2.cvtColor(initial_img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY_INV)[1]
    # finds contours
    _, cont, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    center = []
    radii = []
    for line in cont:
        temp = circle(line)
        center.append(temp[0])
        radii.append(temp[1])

    radii = np.array(radii)
    try:
        ind = np.argmax(radii)  # gets index of largest circle detected
        return center[ind], radii[ind]
    except ValueError:
        print(".............Warning: No Circle Detected.............")


def circle(cnt):
    '''
    Fits contour to a circle

    Parameters:
        cnt: array    | Inputted contour

    Returns:
        center: float | Center of the largest circle detected
        radii: float  | Radiius of the largest circle detected
    '''

    (x, y), radius = cv2.minEnclosingCircle(cnt)
    center = (int(x), int(y))
    radius = int(radius)

    return center, radius
