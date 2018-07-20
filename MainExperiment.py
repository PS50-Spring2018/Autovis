
from ImageCapture import ImageCapture











if __name__=='__main__':
	""" 
    Functionality 
    ---------------------------------------------------------
    get user input for time, intervals and creates instances of analyzer function
    
    Notes: this function needs to run first and from the computer taking  images
	Exit video by clicking into video and pressing ESC key
	Cloud directories facilitate collab
	Exit video by clicking into video and pressing ESC key

    Vars
    ---------------------------------------------------------
    n 			|	Camera number on computer (usually n=0 for built-in webcam)
	dir_file	|	directory of image files
	reaction_id	|	reaction id
	time		|	time to analyze
	interv 		|	interval between image captures
	Processor 	|	the processor class instance
   
    Returns
    ---------------------------------------------------------   
    """ 


	
	dir_file = input("What is the file path?") #raw_input 

	reaction_id=input("What is the reaction ID? ") #integer or string

	time=int(float(input("How long would you like to analyze for (s)? "))) #minutes?
	
	interv=int(float(input("How often do you want to check(s)? ")))

	#constructor
	p=ImageCapture(time,interv, reaction_id, dir_file)
	#this function  runs all iterations of the processor class as defined by the tine and interval
	p.run()
	
    
