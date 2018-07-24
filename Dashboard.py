from matplotlib import pyplot as plt
from matplotlib import image as img
from matplotlib import gridspec as grd
import seaborn as sns
import numpy as np
import colorsys as cs
import cv2

def dashboard(mean_RGB, var_RGB, image_array, N = 100):
	'''
	Display a dashboard containing plots that are relevant to the experiment.
	
	Parameters:
	mean_RGB: 		array 	| mean RGB values for all images taken up to the current point in the experiment
	var_RGB: 		array 	| variances in RGB values for all images taken up to the current point in the experiment
	image_array: 	array 	| latest image of the reaction flask
	N: 				int 	| number of points used to construct the color wheel and color intensity bar
	
	Notes:
	1: N > 200 is not recommended for most laptops.
	2: mean_RGB and var_RGB can be properly formatted by appending mean RBGs and RGB variances to an empty list, then using np.array.
	'''

	# specify a color for each point in HSV space, then convert to RGB for plotting
	radii = np.linspace(0,1,N) 
	thetas = np.linspace(0,2*np.pi,N)
	t = [] 
	r = [] 
	c = []
	for theta in thetas:
		for radius in radii:
			t.append(theta)
			r.append(radius)
			c.append(cs.hsv_to_rgb(theta/(2*np.pi),radius,1)) # all HSV inputs must be 0-1
	
	# specify a color intensity for each x-coordinate in HSV space, then convert to RGB for plotting
	x_dim = np.linspace(0,1,N)
	y_dim = np.linspace(0,1,N)
	x = []
	y = []
	color = []
	for x_val in x_dim:
		for y_val in y_dim:
			x.append(x_val)
			y.append(y_val)
			color.append(cs.hsv_to_rgb(0, 0, 1-x_val)) # rescale for a light-to-dark gradient
	
	# allow the function to be called repeatedly to update the dashboard in real time
	plt.ion()
	plt.close('all')
	
	# construct a 3 X 6 grid and specify grids spanned by each subplot
	gs =grd.GridSpec(3,6) 
	lines = plt.subplot2grid((3,6),(0,0), colspan=2, rowspan =2)
	beaker = plt.subplot2grid((3,6),(0,2), colspan=2, rowspan =2)
	colorbar = plt.subplot2grid((3,6),(2,4), colspan=2)
	squares = plt.subplot2grid((3,6),(2,0), colspan=4)
	colorwheel = plt.subplot2grid((3,6),(0,4), projection = 'polar', colspan=2, rowspan =2) # polar projection for HSV-based color construction
	
	# plot color wheel
	colorwheel.scatter(t, r, c=c, alpha=1.0) # alpha = 1 ensures accurate representation of colors
	colorwheel.xaxis.set_visible(False)
	colorwheel.yaxis.set_visible(False)
	colorwheel.set_title('Tracking through Color Space', fontsize = 8)
	colorwheel.axis('off')
	
	# plot color intensity bar
	colorbar.scatter(x, y, c=color, alpha=1.0) # alpha = 1 ensures accurate representation of color intensities
	colorbar.xaxis.set_visible(False)
	colorbar.yaxis.set_visible(False)
	colorbar.axis('off')
	colorbar.set_title('Tracking through Intensity Space', fontsize = 8)
	
	# set attributes for beaker, lines, and squares plots
	beaker.axis('off')
	beaker.set_title('Latest Beaker Image', fontsize = 8)
	lines.set_title('History of Mean RGB Values', fontsize = 8)
	lines.set_xlabel('Iterations', fontsize = 8)
	squares.axis('off')
	squares.set_title('Mean Color in the Beaker over Time',fontsize = 8)
	
	# plot mean RGB values over the history of the experiment with error bars representing variances
	line_colors = ['r','g','b'] 
	for i, c in enumerate(line_colors):
		lines.errorbar(range(len(mean_RGB)),mean_RGB[:,i],yerr=var_RGB[:,i],color=c)
	
	# display latest image of the reaction flask
	beaker.imshow(image_array, interpolation='nearest') # interpolation = 'nearest' ensures image is displayed accurately
	
	# plot course through color and intensity spaces
	t_val = []
	r_val = []
	v_val = []
	y_val = np.linspace(0,1,len(mean_RGB))
	for color in mean_RGB:
		r, g, b = color[0]/255, color[1]/255, color[2]/255 # rescale RGB values to 0-1 to convert to HSV
		hsv = cs.rgb_to_hsv(r,g,b)
		t_val.append(hsv[0]*2*np.pi) # rescale 0-2*pi for polar plotting
		r_val.append(hsv[1])
		v_val.append(hsv[2])
	colorwheel.plot(t_val,r_val, 'k-')
	colorwheel.plot(t_val[-1],r_val[-1], 'ko')
	colorbar.plot(1-np.array(v_val),y_val,'y-')
	colorbar.plot(1-v_val[-1],y_val[-1],'yo') # plot latest points as circles to show the latest position
	
	# divide squares subplot into horizontal segments based on the number of past mean colors to display and plot those colors
	c_squares = mean_RGB/255 # rescale mean_RGB for the following plot
	for i in range(1,len(mean_RGB)+1):
		squares.plot([i-1+0.49,i-0.49], [0,0], '-', linewidth=100, c=c_squares[i-1])
	
	# display dashboard
	plt.tight_layout() # ensure that plots don't overlap on the dashboard
	plt.show()
	plt.pause(0.05) # allows for the master script to run while the dashboard "waits" (pause) to be called again