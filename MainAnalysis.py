### TO DO!



from Processor import processor


if __name__=='__main__':
	""" 
    Starts the experiment side and gets user input for time, intervals and creates instances of analyzer function.
    
    Parameters used within: 
		n: int 						| 	Camera number on computer (usually n=0 for built-in webcam).
		 
    """ 
	dir_file = input("What is the file path?") #raw_input 

	reaction_id=input("What is the reaction ID? ") #integer or string

	time=int(float(input("How long would you like to analyze for (s)? "))) #minutes?
	
	interv=int(float(input("How often do you want to check(s)? ")))

	#constructor
	p=ImageCapture(time,interv, reaction_id, dir_file)
	#this function  runs all iterations of the processor class as defined by the tine and interval
	p.run()