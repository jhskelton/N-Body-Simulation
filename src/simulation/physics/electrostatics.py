from ..central_potential import CentralPotential

from ... import vector


# define a system of 2nd order ODE system.
# For example:  includes (symplectic Hamiltonian systems)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

k = 1


####  TODO
"""
Need to regularise the system.  Head on collisions result in divergent momenta.
Energy must be conserved with each collision - since it is in the Hamiltonian.
"""


class ElectroStatics(CentralPotential):

	def __init__(self, system, power_law=2):
		self.power_law_potential = power_law
		self.system = system


	def central_force(self, xM, xn, body_M, body_n):
		"""
		Body 'n' attracted to body 'M'

		Gravity:  k = 2
		"""
		k_e = self.power_law_potential # to change later - ATM powerlaw potential

		Q = body_M.charge
		q = body_n.charge

		# calculate displacement vector & norm
		# |r_ji| = | x_j - x_i |
		r = xM - xn
		r_norm = vector.norm( r )

		return ( (-k * Q * q) / (r_norm**(1+k_e)) ) * r



	def central_potential(self, xM, xn, body_M, body_n):
		"""
		Body 'n' attracted to body 'M'

		Gravity:  k = 2
		"""
		k_e = self.power_law_potential # to change later - ATM powerlaw potential

		Q = body_M.charge
		q = body_n.charge

		# calculate displacement vector & norm
		# |r_ji| = | x_j - x_i |
		r = xM - xn
		r_norm = vector.norm( r )

		return ( (k * Q * q) / (r_norm**(k_e-1)) )


