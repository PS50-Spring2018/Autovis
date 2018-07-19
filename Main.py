
from Processor import Processor

"""

n: Camera number on computer (usually n=0 for built-in webcam)
dir_file:
reaction_id:
time:
interv:
Processor:

Exit video by clicking into video and pressing ESC key


Notes: this function needs to run first and from the computer taking  images
Exit video by clicking into video and pressing ESC key
Cloud directories facilitate collab
"""


if __name__=='__main__':
	#get user input for time, interv
	dir_file = input("What is the file path?") #raw_input 

	reaction_id=input("What is the reaction ID? ") #integer or string

	time=int(float(input("How long would you like to analyze for (s)? "))) #minutes?
	
	interv=int(float(input("How often do you want to check(s)? ")))

	#constructor
	p=Processor(time,interv, reaction_id, dir_file)
	#this function  runs all iterations of the processor class as defined by the tine and interval
	p.run()
	
    time=int(float(input("How long would you like to analyze for (s)? "))) #minutes?
    
    interv=int(float(input("How often do you want to check(s)? ")))

    n=int(float(input("Which camera do you want to use, 0 is usually the computer's default camera? ")))
    #constructor
    p=Processor(time,interv, reaction_id, dir_file, n)
    #this function  runs all iterations of the processor class as defined by the tine and interval
    p.run()
    
