""" Script to run data analysis and plotting on the analysis computer """

from CommunicationManager import CommunicationManager


if __name__=='__main__':
    """Runs data analysis and plotting.

    Parameters:
        ...
    """ 

    # Path to image directory
    path = input("Input the path to the image directory: ")

    # Reaction ID
    reaction_id  = input("Input the reaction ID: ")


    # # File path to directory for placing image data
    # dir_file = input("Enter filepath to experiment directory : ")

    # # Reaction ID (Note: this will become the name of the experiment directory)
    # reaction_id = input("Enter Reaction ID : ")

    # # Duration of experiment, in seconds (time window to take images)
    # duration = int(input("Enter duration of experiment [s] : "))
    
    # # Time interval between images
    # img_interval = int(input("Enter interval between images : "))

    # # Type of camera (built-in camera or external webcam)
    # camera_number = int(input("Enter camera number (0 = built-in camera, 1 = external webcam) : "))

    # # Creates instance of ImageCapture event and runs experiment
    # img_expt = ImageCapture(duration, img_interval, reaction_id, dir_file, camera_number)
    # img_expt.run()
    


