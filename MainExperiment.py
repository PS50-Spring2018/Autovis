""" Script to run experiment on the image acquisition computer """

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
    dir_file = input("Enter filepath to experiment directory : ")
    #dir_file = raw_input("Enter filepath to experiment directory : ")

    # Reaction ID (Note: this will become the name of the experiment directory)
    reaction_id = input("Enter Reaction ID : ")
    #reaction_id = raw_input("Enter Reaction ID : ")

    # Duration of experiment, in seconds (time window to take images)
    duration = int(input("Enter duration of experiment [s] : "))
    #duration = int(raw_input("Enter duration of experiment [s] : "))
    
    # Time interval between images
    img_interval = int(input("Enter interval between images : "))
    #img_interval = int(raw_input("Enter interval between images : "))

    # Type of camera (built-in camera or external webcam)
    camera_number = int(input("Enter camera number (0 = built-in camera, 1 = external webcam) : "))
    #camera_number = int(raw_input("Enter camera number (0 = built-in camera, 1 = external webcam) : "))

    # Creates instance of ImageCapture event and runs experiment
    img_expt = ImageCapture(duration, img_interval, reaction_id, dir_file, camera_number)
    img_expt.run()
    

