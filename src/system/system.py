#from . import ODE2

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# put in the ODE system to solve
# ATM the integrator is solving:  d/dt(x)  d/dt(v)
# TODO:  sympletic integrator of Hamiltonian system d/dt(q)  d/dt(p)
#self.ode2 = ODE2.GravPotential(power_law=power_law)

class System:
	def __init__(self, bodies, dim, power_law=2):
		self.N = len(bodies)
		self.d = dim

		self.bodies = bodies
		self.power_law_potential = power_law

		self.update_x0s()
		self.update_v0s()


	def update_x0s(self):
		self.x0s = [ body.x0 for body in self.bodies ]
		if self.N > 0:
			# Extract the implicit dimension of the space
			self.d = len( self.x0s[0] )

	def update_v0s(self):
		self.v0s = [ body.v0 for body in self.bodies ]


	def add_body(self, *bodies):
		self.N += len(bodies)
		self.bodies.extend(bodies)

		self.update_x0s()
		self.update_v0s()


	def remove_body(self, index:int):
		print("System.remove_body()  NOT IMPLEMENTED")









#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
How to make everything have periodic boundary conditions?  
May need to modify things using the bundle/flatten functions - and or the norm function.


"""