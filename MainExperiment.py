
"""Script to start experiment. Takes in user input for data file path, reaction ID, duration, and interval."""

from ImageCapture import ImageCapture


if __name__=='__main__':
    """Runs experiment.

    Parameters:
        dir_file      : string         |   Directory path to image files
        reaction_id   : float/string   |   Reaction identifer
        duration      : int            |   The total time the user would like to take images and analyze for
        img_interval  : int            |   The interval between image captures
        camera_number : int            |   The camera number, 0 for built-in camera and 1 for external webcam
    """ 

    # File path to directory for placing image data
    # Input type : string
    dir_file = input("Enter filepath to experiment directory : ")

    # Reaction ID (Note: this will become the name of the experiment directory)
    # Input type : integer or string
    reaction_id = input("Enter Reaction ID : ")

    # Duration of experiment, in seconds (time window to take images)
    # Input type : integer
    duration = int(input("Enter duration of experiment [s] : "))
    
    # Time interval between images
    # Input type : integer
    img_interval = int(input("Enter interval between images : "))

    # Type of camera (built-in camera or external webcam)
    camera_number = int(input("Enter camera number (0 = built-in camera, 1 = external webcam) : "))

    # Creates instance of ImageCapture event and runs experiment
    img_expt = ImageCapture(duration, img_interval, reaction_id, dir_file, camera_number)
    img_expt.run()
    