""" Dashboard function for plotting """

from matplotlib import pyplot as plt
from matplotlib import image as img
from matplotlib import gridspec as grd
import seaborn as sns
import numpy as np
import colorsys as cs
import cv2


def dashboard(mean_RGB, var_RGB, image_array, N=100):
    '''
    #
    Display a dashboard containing the following information:
    1: time trace of RGB values
    2: image of reaction flask
    3: position on color intensity bar
    4: history of actual color
    5: position on color wheel

    Parameters:
    mean_RGB: 		array 	| mean RGB values for all images taken up
    var_RGB: 		array 	| variances in RGB values for all images taken
    image_array: 	array 	| latest image of the reaction flask
    N: 				int 	| number of points used to construct the color wheel

    Notes:
    1: N > 200 is not recommended for most laptops.
    2: mean_RGB and var_RGB can be properly formatted by appending
    #
    '''

    # construct a 2-dimensional polar space where each point is a color in HSV
    # then convert each point to RGB for plotting
    radii = np.linspace(0, 1, N)
    thetas = np.linspace(0, 2*np.pi, N)
    t = []
    r = []
    c = []
    for theta in thetas:
        for radius in radii:
            t.append(theta)
            r.append(radius)
            # all HSV inputs must be 0-1
            c.append(cs.hsv_to_rgb(theta/(2*np.pi), radius, 1))

    # construct a 2-dimensional Cartesian space where x is a color intensity
    # then convert to RGB for plotting
    x_dim = np.linspace(0, 1, N)
    y_dim = np.linspace(0, 1, N)
    y = []
    color = []
    for x_val in x_dim:
        for y_val in y_dim:
            x.append(x_val)
            y.append(y_val)
            # rescale for a light-to-dark gradient
            color.append(cs.hsv_to_rgb(0, 0, 1-x_val))

    # allow the function to be called repeatedly to update the dashboard
    plt.ion()
    plt.close('all')

    # construct a 3 X 6 grid for plotting
    gs = grd.GridSpec(3, 6)
    lines = plt.subplot2grid((3, 6), (0, 0), colspan=2, rowspan=2)
    beaker = plt.subplot2grid((3, 6), (0, 2), colspan=2, rowspan=2)
    colorbar = plt.subplot2grid((3, 6), (2, 4), colspan=2)
    squares = plt.subplot2grid((3, 6), (2, 0), colspan=4)
    # polar projection for HSV-based color construction
    colorwheel = plt.subplot2grid((3, 6), (0, 4), projection='polar', colspan=2, rowspan=2)

    # plot color wheel
    # alpha = 1 ensures accurate colors
    colorwheel.scatter(t, r, c=c, alpha=1.0)
    colorwheel.xaxis.set_visible(False)
    colorwheel.yaxis.set_visible(False)
    colorwheel.set_title('Tracking through Color Space', fontsize=8)
    colorwheel.axis('off')

    # plot color intensity bar
    # alpha = 1 ensures accurate color intensity
    colorbar.scatter(x, y, c=color, alpha=1.0)
    colorbar.xaxis.set_visible(False)
    colorbar.yaxis.set_visible(False)
    colorbar.axis('off')
    colorbar.set_title('Tracking through Intensity Space', fontsize=8)

    # plot mean RGB values over time with error bars of variances
    line_colors = ['r', 'g', 'b']
    for i, c in enumerate(line_colors):
        lines.errorbar(range(len(mean_RGB)), mean_RGB[:, i], yerr=var_RGB[:, i], color=c)
    lines.set_title('History of Mean RGB Values', fontsize=8)
    lines.set_xlabel('Iterations', fontsize=8)

    # display latest image of the reaction flask
    # interpolation = 'nearest' ensures image is displayed accurately
    beaker.imshow(image_array, interpolation='nearest')
    beaker.axis('off')
    beaker.set_title('Latest Beaker Image', fontsize=8)

    # plot path through color and intensity spaces
    t_val = []
    r_val = []
    v_val = []
    y_val = np.linspace(0, 1, len(mean_RGB))
    for color in mean_RGB:
        #  all RGB values must be 0-1
        r, g, b = color[0]/255, color[1]/255, color[2]/255
        hsv = cs.rgb_to_hsv(r, g, b)
        #  rescale 0-2*pi for polar plotting
        t_val.append(hsv[0]*2*np.pi)
        r_val.append(hsv[1])
        v_val.append(hsv[2])
    colorwheel.plot(t_val, r_val, 'k-')
    colorwheel.plot(t_val[-1], r_val[-1], 'ko')
    colorbar.plot(1-np.array(v_val), y_val, 'y-')
    # plot latest points as circles to show the latest position
    colorbar.plot(1-v_val[-1], y_val[-1], 'yo')

    # display succession of colors over the course of the experiment
    c_squares = mean_RGB/255  # rescale mean_RGB for the following plot
    for i in range(1, len(mean_RGB)+1):
        squares.plot([i-1+0.49, i-0.49], [0, 0], '-', linewidth=100, c=c_squares[i-1])
    squares.axis('off')
    squares.set_title('Mean Color in the Beaker over Time', fontsize=8)
    # display dashboard

    # ensure that plots don't overlap on the dashboard
    plt.tight_layout()
    plt.savefig('TEST.png')
    plt.show()
    # allows for the master script to run while the dashboard "waits"
    plt.pause(0.05)
