""" Script to run data analysis and plotting on the analysis computer """

from CommunicationManager import CommunicationManager


if __name__ == '__main__':
    """
    #
    Runs data analysis and plotting.

    Parameters:
        ...
    #
    """
    # File path to image data, reaction id creates a folder with this name
    dir_file = input("Enter filepath to experiment directory : ")
    reaction_id = input("Enter Reaction ID : ")
    # Creates instance of CommunicationManager class and runs analysis
    manager = CommunicationManager(dir_file, reaction_id)
    manager.initialize()
    manager.run()
