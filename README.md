# Project AutoVis: Automatic Visualization via Webcam

AutoVis is a tool for automating visualization of colored reactions.

## Usage

In practice, two computers are needed, one for running the experiment (i.e. taking images using a built-in camera or an external webcam) and one for running the communication manager that detects the accumulation of image data and initiates the data analysis.

### For taking images on the webcam, execute:

`$ python MainExperiment.py`

The user will input the path to the Dropbox directory, reaction ID, duration of webcam, and image-taking frequency. 

### For initiating the communication manager, execute:

`$ python MainAnalysis.py`

The user will input the path to the Dropbox directory and reaction ID.

### Dependencies and Versions Used
- Python 3.5
- OpenCV
- numpy
- matplotlib
- seaborn
- opencv-python

### Authors

AutoVis was written by Physical Sciences 50 (Spring 2018) at Harvard University. 
