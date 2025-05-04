import scipy.integrate as integrate
import numpy as np

####  TODO:  implement symplectic integrator!

# this looks promising:
# https://pypi.org/project/pyhamsys/


#https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html

class NumericIntegrator:
	def __init__(self):

		# set defaults
		self.max_dt = np.inf
		self.int_method = 'DOP853'

		self.rtol=1e-3
		self.atol=1e-6


	def update_int_method(self, method:str):
		self.int_method = method

	def update_max_dt(self, max_dt:float):
		self.max_dt = max_dt



	def integrate(self, dy_dt, t_range, y0):
		"""
		x
		"""

		# solve the initial value problem
		sol = integrate.solve_ivp( dy_dt, t_range, y0, max_step=self.max_dt, method=self.int_method, atol=self.atol, rtol=self.rtol ) 

		return sol


