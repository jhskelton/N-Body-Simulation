from .. import vector


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Body:
	def __init__(self, pos, vel, mass:float, colour:str, name='', charge=0, static=False, anti_static=False):
		
		self.x0 = vector.vector(pos)
		self.v0 = vector.vector(vel)

		self.is_massless = False
		self.mass = mass

		if mass == 0:
			self.is_massless = True
			self.mass = 1

		self.charge = charge

		self.colour = colour
		self.name = name

		self.static = static
		self.anti_static = anti_static

		






#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def centre_of_mass(bodies, *Xs):
	"""
	Compute the centre of mass x_com

	Xs = [ x1, x2, ..., xN ]
	x = [ x_1, ..., x_d ]
	"""

	N = len(bodies)

	if len(bodies) != len(Xs): raise ValueError("Number of bodies N={0}  &  Number of coordinates = {1}".format(N, len(Xs)))

	X_com = []

	if N > 0:
		d = len(Xs[0])
		if d > 0:
			T = len(Xs[0][0])

			X_com = [ vector.zeroes(T) for i in range(0,d) ]
			masses = [ body.mass for body in bodies ]

			sum_masses = sum(masses)

			for k in range(0,N):
				for i in range(0,d):
					# iterate over all bodies, over all dimensions

					# index the i-th component, add the contribution from the k-th body
					X_com[i] += (masses[k]/sum_masses) * Xs[k][i]
	return X_com

