from ..central_potential import CentralPotential

from ... import vector
from ...arrays import bundle, flatten, flatten_fast



# define a system of 2nd order ODE system.
# For example:  includes (symplectic Hamiltonian systems)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

G = 1
k = 1


####  TODO
"""
Need to regularise the system.  Head on collisions result in divergent momenta.
Energy must be conserved with each collision - since it is in the Hamiltonian.
"""


class GravoElectro(CentralPotential):

	def __init__(self, system, grav_power_law=2, electro_power_law=2):
		self.grav_power_law = grav_power_law
		self.electro_power_law = electro_power_law
		self.system = system


	def central_force(self, xM, xn, body_M, body_n):
		"""
		Body 'n' attracted to body 'M'

		Gravity:  k = 2
		"""
		k_g = self.grav_power_law # to change later - ATM powerlaw potential
		k_e = self.electro_power_law 

		M = body_M.mass
		m = body_n.mass

		Q = body_M.charge
		q = body_n.charge

		# calculate displacement vector & norm
		# |r_ji| = | x_j - x_i |
		r = xM - xn
		r_norm = vector.norm( r )

		return ( ((G * M * m) / (r_norm**(1+k_g))) + (( -k * Q * q) / (r_norm**(1+k_e))) ) * r



	def central_potential(self, xM, xn, body_M, body_n):
		"""
		Body 'n' attracted to body 'M'

		Gravity:  k = 2
		"""
		k_g = self.grav_power_law # to change later - ATM powerlaw potential
		k_e = self.electro_power_law 

		M = body_M.mass
		m = body_n.mass

		Q = body_M.charge
		q = body_n.charge

		# calculate displacement vector & norm
		# |r_ji| = | x_j - x_i |
		r = xM - xn
		r_norm = vector.norm( r )

		return  ((- G * M * m) / (r_norm**(k_g-1))) + (( k * Q * q) / (r_norm**(k_e-1)) )


