from matplotlib import pyplot as plt
from matplotlib import image as img
from matplotlib import gridspec as grd
import seaborn as sns
import numpy as np
import colorsys as cs
import cv2

def dashboard(mean_RGB, var_RGB, image_array, N = 100):

	'''
	The dashboard function should be called continuously to display and update a dashboard containing plots that are relevant to the experiment.
	
	It takes the following inputs:

	mean_RGB is a 3 x N dimensional numpy array of the mean r, g, and b values for all images taken up to the current point in the experiment
	var_RGB is a 3 x N dimensional numpy array of the variances of r, g, and b values for all images taken up to the  current point in the experiment
	image_array is a numpy array representing the latest image of the reaction flask
	N is the number of points used to construct the color wheel and color intensity bar

	Notes:

	1) For most laptop computers, N = 200 is toward the higher end of reasonable computation time for each calling of the function
	Beyond this, improvements to image smoothness are hardly noticeable
	2) One way of accomplishing the proper format for mean_RGB and var_RGB is to create an empty list for each, append the mean RBG and RGB variances for each new image, and convert to a numpy array
	'''

	# Plots the color wheel (radii and thetas together specify every polar coordinate at which the color is specified)
	radii = np.linspace(0,1,N)
	thetas = np.linspace(0,2*np.pi,N)

	# Initializes lists for the following section
	t = [] 
	r = [] 
	c = [] 

	# For each coordinate pair in the polar space, appends the theta and radius for that point, and uses those values to specify the H and S values, respectively, at that point
	# The V value is 1 for every point; together these values specify a color in HSV space (HSV space is used as opposed to RGB space due to its inherently polar construction)
	# Note that theta must be rescaled to 0-1 and the HSV values as a whole must be converted to RGB values scaled 0-1 in order to be taken as an input for the color specification in the scatterplot that follows
	for theta in thetas:
		for radius in radii:
			t.append(theta)
			r.append(radius)
			c.append(cs.hsv_to_rgb(theta/(2*np.pi),radius,1))

	# Plots the color intensity bar (x_dim and y_dim together specify every cartesian coordinate at which the intensity is specified)
	x_dim = np.linspace(0,1,N)
	y_dim = np.linspace(0,1,N)

	# Initializes lists for the following section
	x = []
	y = []
	color = []

	# Similar to nested for-loop above that constructs the color wheel
	# For every coordinate pair in the cartesian space, appends the x- and y- values for that point and uses the x value to specify a V value at that point;
	# H and S values are 0 at every point; together these values specify a color in HSV space
	# Note that these values must be converted to RGB values in order to be taken as an input for the plot that follows
	# Also note that x_val is subtracted from 1 in order to make the plot gradient light to dark (by convention, V values specify colors dark to light from 0 to 1)
	for x_val in x_dim:
		for y_val in y_dim:
			x.append(x_val)
			y.append(y_val)
			color.append(cs.hsv_to_rgb(0, 0, 1-x_val))

	# Turns interactive plotting on, which is necessary due to the function needing to be called repeatedly
	plt.ion()

	# Necessary because this function will be called for each new image
	plt.close('all')

	# Sets up a 3 X 6 grid
	gs =grd.GridSpec(3,6)

	# Names subplots and specifies which grid squares spanned by each
	# Note that the colorwheel projection is changed to polar to accomodate the polar-coordiate-based color scheme from above
	lines = plt.subplot2grid((3,6),(0,0), colspan=2, rowspan =2)
	beaker = plt.subplot2grid((3,6),(0,2), colspan=2, rowspan =2)
	colorbar = plt.subplot2grid((3,6),(2,4), colspan=2)
	squares = plt.subplot2grid((3,6),(2,0), colspan=4)
	colorwheel = plt.subplot2grid((3,6),(0,4), projection = 'polar', colspan=2, rowspan =2)
	
	# Plots the color wheel using the lists populated above
	# Note that alpha = 1 is necessary so that opaque markers provide an accurate representation of colors
	colorwheel.scatter(t, r, c=c, alpha=1.0)
	colorwheel.xaxis.set_visible(False)
	colorwheel.yaxis.set_visible(False)
	colorwheel.set_title('Tracking through Color Space', fontsize = 8)
	colorwheel.axis('off')

	# Plots the color intensity bar using the lists populated above
	# Again, note that alpha = 1 is necessary so that opaque markers provide an accurate representation of colors
	colorbar.scatter(x, y, c=color, alpha=1.0)
	colorbar.xaxis.set_visible(False)
	colorbar.yaxis.set_visible(False)
	colorbar.axis('off')
	colorbar.set_title('Tracking through Intensity Space', fontsize = 8)
	
	# Specifies characteristics of the plots showing the beaker image, RGB plots, and squares depicting the average color in the beaker
	beaker.axis('off')
	beaker.set_title('Latest Beaker Image', fontsize = 8)
	lines.set_title('History of Mean RGB Values', fontsize = 8)
	lines.set_xlabel('Iterations', fontsize = 8)
	squares.axis('off')
	squares.set_title('Mean Color in the Beaker over Time',fontsize = 8)

	# The above sections specify the default appearance of the dashboard
	# The following sections add experiment-specific information to the dashboard 

	# Plot the mean R, G, and B values over the history of the experiment with errorbars representing variances in those values
	line_colors = ['r','g','b']
	for i, c in enumerate(line_colors):
		lines.errorbar(range(len(mean_RGB)),mean_RGB[:,i],yerr=var_RGB[:,i],color=c)

	# Displays the latest image of the beaker
	# Note that interpolation='nearest' is necessary to present the image as is without attempting to interpolate between pixels under certain resolutions
	beaker.imshow(image_array, interpolation='nearest')

	# Initializes lists for the following section
	t_val = []
	r_val = []
	v_val = []
	y_val = np.linspace(0,1,len(mean_RGB))

	# For each RGB triplet, rescales to 0-1 (for the cs.rgb_to_hsv function), convert to HSV (scaled 0-1), rescales theta to 0-2*pi (for polar plotting), and appends to relevant lists
	for color in mean_RGB:
		r, g, b = color[0]/255, color[1]/255, color[2]/255
		hsv = cs.rgb_to_hsv(r,g,b)
		t_val.append(hsv[0]*2*np.pi)
		r_val.append(hsv[1])
		v_val.append(hsv[2]) 

	# Plots course through color and intensity spaces
	# Note that the latest points are plotted as circles to show where the course is currently
	colorwheel.plot(t_val,r_val, 'k-')
	colorwheel.plot(t_val[-1],r_val[-1], 'ko')
	colorbar.plot(1-np.array(v_val),y_val,'y-')
	colorbar.plot(1-v_val[-1],y_val[-1],'yo')

	# Rescales mean_RGB for the following plot
	# x_squares = range(len(mean_RGB)) is this necessary?
	# y_squares = np.zeros(len(x_squares)) is this necessary?
	c_squares = mean_RGB/255

	# Divides a subplot into horizontal segments based on the number of past mean colors to display and plots those colors
	for i in range(1,len(mean_RGB)+1):
		squares.plot([i-1+0.49,i-0.49], [0,0], '-', linewidth=100, c=c_squares[i-1])

	# Ensures that plots don't overlap on the dashboard and allows for the master script to run while the dashboard "waits" (pause) to be called again
	plt.tight_layout() # ensures that plots don't overlap on the dashboard
	plt.show()
	plt.pause(0.05)