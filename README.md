

# Project AutoVis: Automatic Visualization via Webcam

AutoVis is a tool for automating visualization of colored reactions.

## Usage

Two computers are needed, one for running the experiment (i.e. taking images using a built-in camera or an external webcam) and one for running the communication manager that detects the accumulation of image data and initiates the data analysis.

### Computer 1: For taking images on the webcam, execute:

`$ python MainExperiment.py`

The user will input the path to the Dropbox directory, reaction ID, duration of webcam, and image-taking frequency. 

### Computer 2: For initiating the communication manager, execute:

`$ python MainAnalysis.py`

The user will input the path to the Dropbox directory and reaction ID.

## Installation

To install Autovis, the user needs to install the dependencies listed below. 

- For `opencv-python`, we recommend installing via pip: `pip install opencv-python`. For installation on Windows, we recommend following the steps [here](https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_setup/py_table_of_contents_setup/py_table_of_contents_setup.html).

- For `numpy` and `matplotlib`, we recommend installing via pip: `python -m pip install --user numpy matplotlib`. For more detailed instructions, refer to this set of [instructions](https://www.scipy.org/install.html).

- For `seaborn`, we recommend installing via pip: `pip install seaborn`.

Coming soon: we will work on making Autovis pip-installable. 

## Dependencies and Versions Used
- python 3.5
- opencv-python 4.1.0.25
- numpy 1.16.4
- matplotlib 2.2.2
- seaborn 0.8.1

## Key functionalities

![Project Components](ps50algo.PNG)

## Authors

AutoVis was written by Physical Sciences 50 (Spring 2018) at Harvard University. 
