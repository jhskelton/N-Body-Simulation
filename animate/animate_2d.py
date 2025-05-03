import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import matplotlib.colors as colors

import numpy as np

#plt.rcParams['animation.ffmpeg_path'] = '.venv/lib/python3.12/site-packages/ffmpeg'

import matplotlib.animation as animation
#import ffmpeg


"""
TODO:

Implement a (dynamical) coordinate transformation.
The following should be pre-processed!  Not while plotting.
	- centre of mass frame
	- put one particle centre of frame

Process while plotting:
	- continuously rotating coordinate system - eg tail moves backwards
	- eg rotate a drawn figure [draw a shape, then rotate it]

"""


"""
Nice Colours for matplotlib on black background

deepskyblue
dodgerblue

limegreen
"""


"""
TODO:  I want to plot with faded trails!
"""

"""

class Animate2dOrbit:
	def __init__(x,y):
		self.x = x
		self.y = y

		self.trail_len = -1
		self.dark_mode = True

		self.xlim = None
		self.ylim = None

		self.colour = 'white'

	def new_canvas(dark_mode=True, xis_off=True, xlim=None, ylim=None):

		if dark_mode:
"""

"""

	# Want to try to use this...
	# https://stackoverflow.com/questions/71932611/making-fading-trails-in-python-funcanimation
	#green = colors.to_rgb("limegreen") + (0.0,)
	#greenfade = colors.LinearSegmentedColormap.from_list('my', [green, "limegreen"])

"""



def animate_2d_orbits(xs,ys, 
					  colours=None, linewidths=None, markersizes=None,
					  trail_len=-1, plt_style='dark_background', axis_off=True, 
					  xlim=None, ylim=None, 
					  interval = 70,
					  coord_transform=lambda *x: x):
	"""
	Assume Inpute is a collection of x & y coordinates of N bodies

	xs = [x1, x2,..., xN]
	ys = [y1, y2,..., yN]

	where xk = [xk1, xk2, ..., xkn] etc

	likewise, colours= [colour1, colour2, .., colourN]
	if colours=None, then just do default colourscheme
	"""

	N = len(xs)   # number of particles
	Ny = len(ys)
	T = 0         # number of time series elements


	# raise some exceptions
	if N != Ny:
		raise Exception("input xs and ys do not have the same length")
	if N < 1:
		raise Exception("Empty x list, nothing to plot")


	# check the xs and ys is indeed a list of lists
	try:
		len(xs[0])
	except TypeError:
		xs = [xs]; ys = [ys]
		N = 1
	
	# get the number of elements!
	T = len(xs[0])


	for i in range(0, N):
		if len(xs[i]) != T:
			raise Exception("The x-position of the {0}-th and 1st particles do not have equal time series elements".format(i))

	for i in range(0, N):
		if len(ys[i]) != T:
			raise Exception("The y-position of the {0}-th and 1st particles do not have equal time series elements".format(i))


	if type(colours) == type(list):
		if len(colours) != N:
			raise Exception("Number of selected colours does not match number of objects to animate")
	
	if type(markersizes) == type(list):
		if len(markersizes) != N:
			raise Exception("Number of marker sizes does not match number of objects to animate")
	
	if type(linewidths) == type(list):
		if len(linewidths) != N:
			raise Exception("Number of linewidths does not match number of objects to animate")


	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	###  MAIN


	#https://matplotlib.org/stable/gallery/style_sheets/style_sheets_reference.html#sphx-glr-gallery-style-sheets-style-sheets-reference-py
	plt.style.use(plt_style)

	artists = []

	fig, ax = plt.subplots()
	if axis_off:
		ax.axis('off')
	else:
		ax.set_xlabel("x")
		ax.set_ylabel("y")


	if type(xlim) == list:
		ax.set_xlim(xlim)
	if type(ylim) == list:
		ax.set_ylim(ylim)



	for t in range(0, T):
		# iterate over time series element

		# container of all the 2d lines to plot on a single frame
		container = []


		for i in range(0,N):
			# iterate over every particle

			start_pos = 0
			if trail_len >= 0:
				start_pos =  max(0, t-trail_len)  # so don't -1 index 

			x = xs[i][start_pos:t+1]
			y = ys[i][start_pos:t+1]


			# transform the coordinates
			x,y,_ = coord_transform(x,y,t)

			# add plots to the frame container

			lw = 2
			mksize = 10
			colour = None

			if type(colours) != type(None):
				colour = colours[i]

			if type(linewidths) != type(None):
				lw = linewidths[i]
			if type(markersizes) != type(None):
				mksize = markersizes[i]

			container.append( ax.plot(x, y, color=colour, linewidth=lw)[0] )
			container.append( ax.plot(x[-1],y[-1], 'o', color=colour, markersize=mksize)[0] )

		
		artists.append(container)

	anim = animation.ArtistAnimation(fig=fig, artists=artists, interval=interval)

	return anim













def animate_2d_plots(xs, ys, 
					  colours=None, linewidths=None, markersizes=None,
					  trail_len=-1, plt_style='default', axis_off=False, 
					  xlim=None, ylim=None, 
					  interval = 70,
					  xlabel="",ylabel="",title=""):
	"""
	Assume Inpute is a collection of x & y coordinates of N bodies

	xs = [x1, x2,..., xN]
	ys = [y1, y2,..., yN]

	where xk = [xk1, xk2, ..., xkn] etc

	likewise, colours= [colour1, colour2, .., colourN]
	if colours=None, then just do default colourscheme
	"""

	N = len(xs)   # number of particles
	Ny = len(ys)
	T = 0         # number of time series elements


	# raise some exceptions
	if N != Ny:
		raise Exception("input xs and ys do not have the same length")
	if N < 1:
		raise Exception("Empty x list, nothing to plot")


	# check the xs and ys is indeed a list of lists
	try:
		len(xs[0])
	except TypeError:
		xs = [xs]; ys = [ys]
		N = 1
	
	# get the number of elements!
	T = len(xs[0])


	for i in range(0, N):
		if len(xs[i]) != T:
			raise Exception("The x-position of the {0}-th and 1st particles do not have equal time series elements".format(i))

	for i in range(0, N):
		if len(ys[i]) != T:
			raise Exception("The y-position of the {0}-th and 1st particles do not have equal time series elements".format(i))


	if type(colours) == type(list):
		if len(colours) != N:
			raise Exception("Number of selected colours does not match number of objects to animate")
	
	if type(markersizes) == type(list):
		if len(markersizes) != N:
			raise Exception("Number of marker sizes does not match number of objects to animate")
	
	if type(linewidths) == type(list):
		if len(linewidths) != N:
			raise Exception("Number of linewidths does not match number of objects to animate")


	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	###  MAIN


	#https://matplotlib.org/stable/gallery/style_sheets/style_sheets_reference.html#sphx-glr-gallery-style-sheets-style-sheets-reference-py
	plt.style.use(plt_style)

	artists = []

	fig, ax = plt.subplots()
	if axis_off:
		ax.axis('off')
	else:
		ax.set_xlabel("x")
		ax.set_ylabel("y")


	if type(xlim) == list:
		ax.set_xlim(xlim)
	if type(ylim) == list:
		ax.set_ylim(ylim)

	if xlabel != "":
		ax.set_xlabel(xlabel)
	if ylabel != "":
		ax.set_ylabel(ylabel)
	if title != "":
		ax.set_title(title)



	for t in range(0, T):
		# iterate over time series element

		# container of all the 2d lines to plot on a single frame
		container = []


		for i in range(0,N):
			# iterate over every particle

			start_pos = 0
			if trail_len >= 0:
				start_pos =  max(0, t-trail_len)  # so don't -1 index 

			x = xs[i][start_pos:t+1]
			y = ys[i][start_pos:t+1]

			# add plots to the frame container

			lw = 2
			mksize = 10
			colour = None

			if type(colours) != type(None):
				colour = colours[i]

			if type(linewidths) != type(None):
				lw = linewidths[i]
			if type(markersizes) != type(None):
				mksize = markersizes[i]

			container.append( ax.plot(x, y, color=colour, linewidth=lw)[0] )
			container.append( ax.plot(x[-1],y[-1], 'o', color=colour, markersize=mksize)[0] )

		
		artists.append(container)

	anim = animation.ArtistAnimation(fig=fig, artists=artists, interval=interval)

	return anim


