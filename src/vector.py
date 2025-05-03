import numpy as np



def vector(array):

	# two options:
	# 1) array is a list of numeric data
	# 2) array is a list of lists

	# see if the array elements are indexable
	indexable = False
	try:
		array[0][0]
		indexable = True
	except TypeError:
		pass
	except IndexError:
		pass

	if indexable:
		return [ vector(array[i]) for i in range(0,len(array)) ]
	else:
		return np.array(array, dtype=np.float64)


def zeroes(d:int):
	return vector( [0]*d )

def subtract(x, *y):
	"""
	y = [ y1, y2, ..., yn ]
	Compute yi - x

	x & yi are each vector objects
	"""
	return [ y[i] - x for i in range(0,len(y)) ]



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def inner_prod(a,b):
	out = 0

	if len(a) != len(b):
		raise ValueError()

	for i in range(0,len(a)):
		# standard euclidean inner product
		out += np.multiply( a[i], b[i] )

	return out



def norm(a):
	return np.sqrt( inner_prod(a,a) )




