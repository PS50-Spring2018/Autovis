""" Script to run data analysis and plotting on the analysis computer """

from CommunicationManager import CommunicationManager


if __name__=='__main__':
    """Runs data analysis and plotting.

    Parameters:
        ...
    """ 

    # File path to image data
    dir_file = raw_input("Enter filepath to experiment directory : ")

    # Reaction ID (Note: this is the name of the experiment directory)
    reaction_id = raw_input("Enter Reaction ID : ")

    # Creates instance of CommunicationManager class and runs analysis
    manager = CommunicationManager(dir_file, reaction_id)
    manager.initialize()
    manager.run()
