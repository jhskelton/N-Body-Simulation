from . import vector

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#xs[i] = vector( xvs_flat[ i*d : (i+1)*d ] )
#vs[i] = vector( xvs_flat[ (N+i)*d : (N+i+1)*d ] )
#vs[i] = xvs_flat[ (N+i)*d : (N+i+1)*d ]

#out[(N+n)*d + i] = vs[n][i]





"""
Need to figure out how to speed up the below functions!
"""


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def bundle_fast(Xs_flat, k, N,d):
	"""
	#k arrays of
	#N arrays of N bodies of
	#d dimensional arrays of d numerical values

	#eg Xs = [ x, v ]
	#x = [ x1, x2, ..., xN ]
	#x1 = [ (x1)_1, ..., (x1)_d ]
	"""
	Xs = [ [None]*N for i in range(0,k) ]

	if len(Xs_flat) != N*d*k:
		raise ValueError()

	for j in range(0,k):
		for i in range(0,N):
			Xs[j][i] = Xs_flat[ (j*N+i)*d : (j*N+i+1)*d ]
			
	return Xs





def flatten_fast(*Xs):
	"""
	*Xs = [ x, v, w, ... ]
	x = [ x1, x2, .., xN ]
	x1 = [ (x1)_1, ..., (x1)_d]

	Construct 'flat' array of numeric values

	Xs_flat = [ (x1)_1, (x1)_2, ..., (x1)_d, (x2)_1, ..., (xN)_d, (v1)_1, ... ]
	"""

	L = len(Xs)
	Xs_flat = []

	if L > 0:
		# assume all the xs in Xs are equal length of N

		N = len(Xs[0])

		if N > 0:
			d = len(Xs[0][0])
			Xs_flat = vector.zeroes( N * d * L )

			for j in range(0,L):
				for n in range(0,N):
					for i in range(0,d):
						Xs_flat[ (j*N+n)*d + i] = Xs[j][n][i]
	return Xs_flat





#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def bundle(Xs_flat, *dims):
	"""
	k arrays of
	N arrays of N bodies of
	d dimensional arrays of d numerical values

	eg Xs = [ x, v ]
	x = [ x1, x2, ..., xN ]
	x1 = [ (x1)_1, ..., (x1)_d ]
	"""

	out = Xs_flat

	if len(dims) == 0:
		print("WARNING:  bundle function called with no bundling dimensions")

	else:
		N = dims[0]

		remain_dim = 1
		for i in range(1,len(dims)):
			remain_dim *= dims[i]

		tot_dim = remain_dim * N

		if N == tot_dim:
			# bundle vector of dim N into vector of dim N - ie do nothing

			pass

		else:
			# check inpute is well defined
			if tot_dim != len(Xs_flat):
				raise ValueError("Cannot bundle length={0} object into dimensions {1}".format(len(Xs_flat), dims))

			# recurvsive Algorthim
			Xs = [ None ] * N

			for i in range(0, N):
				Xs[i] = bundle( Xs_flat[ i*remain_dim: (i+1)*remain_dim ] , *dims[1:len(dims)] )
			out = Xs
	return out



def flatten(depth:int, *Xs):
	"""
	*Xs = [ x, v, w, ... ]
	x = [ x1, x2, .., xN ]
	x1 = [ (x1)_1, ..., (x1)_d]

	Construct 'flat' array of numeric values

	Xs_flat = [ (x1)_1, (x1)_2, ..., (x1)_d, (x2)_1, ..., (xN)_d, (v1)_1, ... ]

	In this example, depth=2

	depth = number of times to flatten
	"""
	if depth <= 0:
		return Xs   # no more flattening needed

	L = len(Xs)
	Xs_flat = []

	if L > 0:
		if depth > 1:
			# flatten recursively
			Xs = [flatten(depth-1, *Xs[i]) for i in range(0,L) ]

		# want to flatten the single array

		# assume all the xs in Xs are equal length of N
		N = len(Xs[0])

		if N>0:
			Xs_flat = [ None ] * N * L

			for i in range(0,L):
				for j in range(0,N):
					Xs_flat[ i*N + j ] = Xs[i][j]

	return Xs_flat


