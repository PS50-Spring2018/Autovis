""" Script to run experiment on lab computer """

from ImageCapture import ImageCapture


if __name__ == '__main__':
    """
    Runs experiment.

    Parameters:
        dir_file    : string    | Directory path to image files
        rxn_id      : string    | Reaction identifer
        duration    : int       | The total time of experiment
        img_interval: int       | The interval between image captures
        camera_num  : int       | 0 for built-in  and 1 for external
    """

    # File path to directory for placing image data
    dir_file = input("Enter filepath to experiment directory : ")
    # dir_file = raw_input("Enter filepath to experiment directory : ")

    # Reaction ID, this will become the name of the experiment directory)
    rxn_id = input("Enter Reaction ID : ")
    # reaction_id = raw_input("Enter Reaction ID : ")

    # Duration of experiment, in seconds
    dur = int(input("Enter duration of experiment [s] : "))

    # Time interval between images
    img_interval = int(input("Enter interval between images : "))

    # Type of camera (built-in or external)
    camera_num = int(input("Enter camera # (0 = built-in , 1 = external): "))

    # Creates instance of ImageCapture runs experiment
    img_expt = ImageCapture(dur, img_interval, rxn_id, dir_file, camera_num)
    print('Running experiment...')
    img_expt.run()
    print('Experiment finished!')
