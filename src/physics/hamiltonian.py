from abc import ABC, abstractmethod
#https://docs.python.org/3/library/abc.html

import numpy as np
import scipy.integrate as integrate

from ..arrays import flatten_fast, bundle, flatten




class DynamicalSystem(ABC):

	@abstractmethod
	def dy_dt(self,t,y):
		pass

	def solve_ivp(self, t_fin, y0, numeric_solver):

		sol = numeric_solver.integrate( self.dy_dt, [0,t_fin], y0 ) 
		t = sol.t
		y = sol.y

		return y,t




class Hamiltonian(DynamicalSystem):
	
	@abstractmethod
	def dp_dt(self, t, x, p):
		pass

	@abstractmethod
	def dx_dt(self, t, x, p):
		pass

	@abstractmethod
	def hamiltonian(self, t, x, p):
		pass


	@abstractmethod
	def v2p(self, t, x, p):
		pass
	@abstractmethod
	def p2v(self, t, x, p):
		pass



	def dy_dt(self, t, xps ):
		"""
		AKA: dxp_dt_flat

		Array of [ x_1,1  x_1,2  ... x_1,d  x_2,1 ... x_N,d  p_1,1  ... p_N,d ]
		"""
		# define the function:  f(t,y) = dy/dx

		N = len(xps) // 2
		xs, ps = bundle(xps, 2,N)

		dxdt = self.dx_dt(t, xs, ps)
		dpdt = self.dp_dt(t, xs, ps)

		# dxdt are already flat arrays

		return flatten(1, dxdt,dpdt)



	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	#
	#   Numerical Solver


	def solve(self, t_fin, x0s, p0s, numeric_solver):
		"""
		Let x0s & p0s be two 'flat' arrays of initial positions and momenta
		"""
		if len(x0s) != len(p0s):
			raise ValueError("Number of x & p coordinates ({0} & {1}) do not match in Hamiltonian.Solve".format(len(x0s), len(p0s)))

		H = self.hamiltonian(0,x0s,p0s)
		
		# construct the initial conditions - flatten the x & y of N-bodies into single array
		xp0s_flat = flatten(1,x0s,p0s)

		# solve the initial value problem
		y,t = self.solve_ivp(t_fin, xp0s_flat, numeric_solver)

		N = len(y) // 2
		xs,ps = bundle(y,2,N)

		return xs,ps,t


"""

	def solve_xv(self, t_fin, x0s, v0s, numeric_solver):
		""
		Solve system with initial positions and velocities
		""

		# Convert initial velocities to momentum

		p0s = self.v2p(0,x0s,v0s)

		xs,ps,t = self.solve_xp(t_fin, x0s, p0s, numeric_solver)

		vs = self.p2v(t, xs,ps)

		if len(vs) != len(ps):
			raise Exception("Hamiltonian.p2v() is not implemented correctly. Converted dim={0} vector into dim={1} vector.".format(len(ps),len(vs)))

		return xs,vs,t
"""
