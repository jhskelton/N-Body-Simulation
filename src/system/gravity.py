from .central_potential import CentralPotential

from .. import vector
from ..arrays import bundle, flatten, flatten_fast



# define a system of 2nd order ODE system.
# For example:  includes (symplectic Hamiltonian systems)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

G = 1


####  TODO
"""
Need to regularise the system.  Head on collisions result in divergent momenta.
Energy must be conserved with each collision - since it is in the Hamiltonian.
"""


class Gravity(CentralPotential):

	def __init__(self, system, power_law=2):
		self.power_law_potential = power_law
		self.system = system


	def central_force(self, xM, xn, body_M, body_n):
		"""
		Body 'n' attracted to body 'M'

		Gravity:  k = 2
		"""
		k = self.power_law_potential # to change later - ATM powerlaw potential

		M = body_M.mass
		m = body_n.mass

		# calculate displacement vector & norm
		# |r_ji| = | x_j - x_i |
		r = xM - xn
		r_norm = vector.norm( r )

		return ( (G * M * m) / (r_norm**(1+k)) ) * r



	def central_potential(self, xM, xn, body_M, body_n):
		"""
		Body 'n' attracted to body 'M'

		Gravity:  k = 2
		"""
		k = self.power_law_potential # to change later - ATM powerlaw potential

		M = body_M.mass
		m = body_n.mass

		# calculate displacement vector & norm
		# |r_ji| = | x_j - x_i |
		r = xM - xn
		r_norm = vector.norm( r )

		return (-G * M * m) / (r_norm**(k-1))


