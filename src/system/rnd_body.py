import random as rnd

from .. import vector
from .body import Body




#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def generate_random_bodies(N:int, d:int, r_max:float, v_max:float, mass:float, colour:str='white', charge:float=0, mass_var:float=0.0, charge_var:float=0.0, static=False, anti_static=False):
	# Generate random bodies uniformly in a ball of radius r_max & velocity v_max

	# TODO make sampling uniform. atm implements to just get it to work

	bodies = []

	for i in range(0,N):
		# sample random body

		x0 = vector.vector( [ rnd.uniform(-r_max, r_max) for j in range(0,d) ] )

		v0 = vector.vector( [ rnd.uniform(-v_max, v_max) for j in range(0,d) ] )

		m = rnd.uniform(mass-mass_var, mass+mass_var)
		q = rnd.uniform(charge-charge_var, charge+charge_var)

		bodies.append( Body(x0, v0, mass=m, colour=colour, name='rnd{0}'.format(i), charge=q, anti_static=anti_static, static=static) )

	return bodies


