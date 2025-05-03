import numpy as np
from scipy.interpolate import CubicSpline



def interpolate_timestep(xs,t, dt, spline=True):
	"""
	Let xs be nested arrays of x(t). Where x(t) is an array of numerical values.
	ie x is a function of t.

	Geneically, the difference between two sequential elements in t may not be constant.
	e.g. t = [1,2,4,5]
	
	Want to output x(T)
	where T = [t0, t0+dt, t0+2dt + ... ]
	"""

	# recursively go through each of the sub-arrays

	# no interpolation if dt is None
	if type(dt) == type(None):
		return xs,t

	# else proceed as normal

	t0 = t[0]
	tN = t[-1]
	N = int((tN-t0) / dt) + 1

	T = np.linspace(t0, tN, N)


	def interpolation( x ):
		x_interp = []

		if spline:
			I = CubicSpline(t,x)
			x_interp = I(T)

		else:
			#https://docs.scipy.org/doc/scipy/tutorial/interpolate/1D.html#tutorial-interpolate-1dsection
			x_interp = np.interp(T, t, x)

		return x_interp


	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	def recursive_routine( xs ):
		out = []
		N = len(xs)

		if N > 0:
			try:
				len(xs[0])  # if no error then xs is an array of arrays

				out = [ recursive_routine(x) for x in xs ]

			except TypeError:
				# xs is an honest array of numeric values
				out = interpolation( xs )

		return out

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	return recursive_routine( xs ), T
	


