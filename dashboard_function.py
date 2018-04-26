from matplotlib import pyplot as plt
from matplotlib import image as img
from matplotlib import gridspec as grd
import seaborn as sns
import numpy as np
import colorsys as cs
import cv2

def dashboard(mean_RGB, var_RGB, image_array, N =100):
	# the dashboard function is run continuously to display and update a dashboard containing plots that are relevant to the experiment
	# it takes the following inputs:

	# mean_RGB is a 3 x N dimensional numpy array of ** all-time ** mean r, g, and b values for each image
	# var_RGB is a 3 x N dimensional numpy array of ** all-time ** variances in r, g, and b values for each image
	# image_array is a numpy array representing the latest image of the beaker
	# N is the number of points used to construct the color wheel and intensity bar

	# notes:
	# 1) we highly recommend using no larger than N = 200, as this is will add significant computation time to each calling of the function
	# and the visual difference is negligible
	# 2) one way of accomplishing the proper format for mean_RGB and var_RGB is to create an empty list for each and for each new image,
	# append the mean RGB values and RGB variances for that image, and finally convert to a numpy array

	# the following section plots the color wheel
	radii = np.linspace(0,1,N)
	thetas = np.linspace(0,2*np.pi,N) # radii and thetas together specify every polar coordinate at which the color will be specified

	# initializing lists for the following section
	t = [] 
	r = [] 
	c = [] 

	# for each coordinate pair in the polar space, append the theta and radius for that point, and use those values to specify 
	# the h and s values, respectively, at that point; the v value is 1 for every point; together these values specify a color
	# however, theta must be rescaled to 0-1 and the hsv values as a whole must be converted to rgb values scaled 0-1 in order
	# to be taken as an input for the color specification in the scatterplot that follows
	for theta in thetas: #nested for-loop
		for radius in radii:
			t.append(theta)
			r.append(radius)
			c.append(cs.hsv_to_rgb(theta/(2*np.pi),radius,1)) #rescale theta to 0-1
			# 1 at the end corresponds to intensity

	# the following section plots the color bar
	x_dim = np.linspace(0,1,N)
	y_dim = np.linspace(0,1,N) # x_dim and y_dim together specify every cartesian coordinate at which the intensity will be specified

	# initializing lists for the following section
	x = []
	y = []
	color = []

	# very similar to nested for-loop above that constructs the color wheel
	# for every coordinate pair in the cartesian space, append the x and y values for that point, and use the x value to specify
	# a v value at that point; h and s values are 0 at every point; together these values specify a color
	# however, these values must be converted to rgb values in order to be taken as an input for the plot that follows 
	for x_val in x_dim:
		for y_val in y_dim:
			x.append(x_val)
			y.append(y_val)
			color.append(cs.hsv_to_rgb(0, 0, 1-x_val)) # x_val subtracted from 1 in order to make the plot light to dark as opposed to 
			# dark to light (which is just convention for v values in hsv)

	# Turn interactive plotting on
	plt.ion()
	# plt.close is necessary because this function will be called for each new image
	plt.close('all')
	# sets up grid
	gs =grd.GridSpec(3,6)
	# specifies which grid squares each subplot spans
	lines = plt.subplot2grid((3,6),(0,0), colspan=2, rowspan =2)
	beaker = plt.subplot2grid((3,6),(0,2), colspan=2, rowspan =2)
	colorbar = plt.subplot2grid((3,6),(2,4), colspan=2)
	squares = plt.subplot2grid((3,6),(2,0), colspan=4)
	colorwheel = plt.subplot2grid((3,6),(0,4), projection = 'polar', colspan=2, rowspan =2)
	
	# plots the color wheel using the lists populated above
	colorwheel.scatter(t, r, c=c, alpha=1.0) # alpha = 1.0 is necessary so that opaque markers provide an accurate representation of the colors
	colorwheel.xaxis.set_visible(False)
	colorwheel.yaxis.set_visible(False)
	colorwheel.set_title('Tracking through Color Space', fontsize = 8)
	colorwheel.axis('off')

	# plots the color bar using the lists populated above
	colorbar.scatter(x, y, c=color, alpha=1.0) # alpha = 1.0 is necessary so that opaque markers provide an accurate representation of the colors
	colorbar.xaxis.set_visible(False)
	colorbar.yaxis.set_visible(False)
	colorbar.axis('off')
	colorbar.set_title('Tracking through Intensity Space', fontsize = 8)
	
	# specifies characteristics of the plots showing the beaker image, rgb plots, and squares depicting the average color in the beaker
	beaker.axis('off')
	beaker.set_title('Latest Beaker Image', fontsize = 8)

	lines.set_title('History of Mean RGB Values', fontsize = 8)
	lines.set_xlabel('Iterations', fontsize = 8)
	
	squares.axis('off')
	squares.set_title('Mean Color in the Beaker over Time',fontsize = 8)

	# the above sections specify the "default" appearance of the dashboard
	# the following sections add experiment-specific information to the dashboard 

	# plots the mean r, g, and b values over the history of the experiment with errorbars representing variances in those values
	line_colors = ['r','g','b']
	for i, c in enumerate(line_colors):
		lines.errorbar(range(len(mean_RGB)),mean_RGB[:,i],yerr=var_RGB[:,i],color=c)

	# displays the latest image of the beaker
	beaker.imshow(image_array, interpolation='nearest')

	# initializing lists for the following section, which plots course through color and intensity spaces
	t_val = []
	r_val = []
	v_val = []
	y_val = np.linspace(0,1,len(mean_RGB))

	# for each RGB triplet, rescale to 0-1 (for the cs.rgb_to_hsv function), convert to hsv (scaled 0-1), rescale theta to 0-2pi,
	# then append to relevant lists
	for color in mean_RGB:
		r, g, b = color[0]/255, color[1]/255, color[2]/255
		hsv = cs.rgb_to_hsv(r,g,b)
		t_val.append(hsv[0]*2*np.pi)
		r_val.append(hsv[1])
		v_val.append(hsv[2]) 

	# plots course through color and intensity spaces
	colorwheel.plot(t_val,r_val, 'k-')
	colorwheel.plot(t_val[-1],r_val[-1], 'ko') # adds last point as a circle to show where the course ends
	colorbar.plot(1-np.array(v_val),y_val,'y-')
	colorbar.plot(1-v_val[-1],y_val[-1],'yo') # adds last point as a circle to show where the course ends

	# sets up lists to show history of average colors in the next section
	x_squares = range(len(mean_RGB))
	y_squares = np.zeros(len(x_squares))
	c_squares = mean_RGB/255

	# divides a plot into horizontal segments according to the number of past mean colors to display
	for i in range(1,len(mean_RGB)+1):
		squares.plot([i-1+0.49,i-0.49], [0,0], '-', linewidth=100, c=c_squares[i-1])

	plt.tight_layout() # ensures that plots don't overlap on the dashboard
	plt.show()
	plt.pause(0.05) # hack: rest of master script is run while the plot "waits" to be called again