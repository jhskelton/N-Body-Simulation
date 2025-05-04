from ..simulation.hamiltonian import Hamiltonian
from abc import ABC, abstractmethod
import numpy as np

from .. import vector
from ..arrays import bundle, flatten, flatten_fast



# define a system of 2nd order ODE system.
# For example:  includes (symplectic Hamiltonian systems)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


####  TODO
"""
Need to regularise the system.  Head on collisions result in divergent momenta.
Energy must be conserved with each collision - since it is in the Hamiltonian.
"""


class CentralPotential(Hamiltonian):

	@abstractmethod
	def central_potential(self, xM, xn, body_M, body_n):
		pass

	@abstractmethod
	def central_force(self, xM, xn, body_M, body_n):
		pass


	# Defined methods

	def hamiltonian_NBody(self, t, xs, ps):
		"""
		Assume xs & ps bundled up into
		[ x1, .., xN ]
		where x1 = [ (x1)_1, (x1)_2, ..., (x1)_d ]
		"""
		xs_flat = flatten(2, xs)
		ps_flat = flatten(2, ps)

		return self.hamiltonian(t, xs_flat, ps_flat)


	def hamiltonian(self, t, xs, ps):
		"""
		Assume flat input.  Array of 
		[ x_1,1  x_1,2  ... x_1,d  x_2,1 ... x_N,d ]  
		[ p_1,1  ... p_N,d ]
		"""

		#  Need to bundle & flatten arrays - so can work with displacement vectors
		N = self.system.N
		d = self.system.d

		bodies = self.system.bodies
		masses = [ bodies[i].mass for i in range(0,N) ]

		# bundle into N vectors, each of dimension d
		xs = np.array( bundle(xs, N, d) )
		ps = np.array( bundle(ps, d, N) )

		# bundle into array [ (xs)_1, ... (xs)_d ]
		# so then p_norm = [ xs_norm ] = [ x1_norm, x2_norm, ... xN_norm ]

		#####  kinetic: p^2/(2m)

		p_norm = vector.norm(ps)
		p_sq = np.power( p_norm, 2)

		kinetic = 0 #vector.zeroes( len(t) ) 

		try:
			# warning! size-one arrays become numerics! So p_norm will not be a 2d-array!
			if N==1:
				kinetic = p_sq/(2*masses[0])

			else:
				p_sq_on_m = [ p_sq[i]/(2*masses[i]) for i in range(0,N) ]

				for i in range(0,N):
					kinetic += p_sq_on_m[i]
		except IndexError:
			pass

		#####  now compute the potential term

		U = 0 #vector.zeroes( len(kinetic) )
		for i in range(0,N):
			for j in range(i+1,N):
				Uij = self.central_potential( xs[i],xs[j],bodies[i],bodies[j] )
				U+= Uij

		H = kinetic + U
		return H


	def initial_hamiltonian(self):

		x0s = self.system.x0s
		v0s = self.system.v0s

		x0s_flat = flatten_fast(x0s)
		v0s_flat = flatten_fast(v0s)

		p0s_flat = self.v2p(0, x0s_flat, v0s_flat)
		N = self.system.N
		d = self.system.d

		p0s = bundle(p0s_flat, N,d)

		return self.hamiltonian_NBody(0, x0s, p0s)



	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


	def p2v(self, t, xs, ps):
		"""
		Array of 
		[ x_1,1  x_1,2  ... x_1,d  x_2,1 ... x_N,d ]  
		[ p_1,1  ... p_N,d ]
		"""
		# v = p/m

		N = self.system.N
		d = self.system.d

		out = vector.vector( ps )
		for i in range(0,N):      # iterate over all N bodies
			for j in range(0, d): # iterate over all d dimensions

				out[ i*d + j ] /= self.system.bodies[i].mass
		return out


	def v2p(self, t, xs, vs):
		"""
		Array of 
		[ x_1,1  x_1,2  ... x_1,d  x_2,1 ... x_N,d ]  
		[ v_1,1  ... v_N,d ]
		"""
		# p = mv

		N = self.system.N
		d = self.system.d

		out = vector.vector( vs )
		for i in range(0,N):      # iterate over all N bodies
			for j in range(0, d): # iterate over all d dimensions

				out[ i*d + j ] *= self.system.bodies[i].mass
		return out


	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


	def dx_dt(self, t, xs, ps):
		return self.p2v(t,xs,ps)


	def dp_dt(self, t, xs, ps):

		#  Need to bundle & flatten arrays - so can work with displacement vectors
		N = self.system.N
		d = self.system.d

		# bundle into N vectors, each of dimension d
		xs = bundle(xs, N, d)

		out = []
		if N>0:
			# array of zero vectors
			#out = [ vector.zeroes(N) for i in range(0,N) ]
			out = vector.zeroes(N*d)

		for i in range(0,N):      # iterating over all N-bodies
			for j in range(i+1,N):  # iterate over remaining bodies (not n)
				# j > i

				bod_j = self.system.bodies[j]
				bod_i = self.system.bodies[i]

				# check whether to update dp_dt for the bodies. ie if static or anti-static.
				update_i = True
				update_j = True

				update_i = update_i and (not bod_i.static or (bod_j.static and bod_i.static != bod_j.static))
				update_j = update_j and (not bod_j.static or (bod_i.static and bod_i.static != bod_j.static))

				update_i = update_i and (not bod_j.anti_static or (bod_i.anti_static and (bod_i.anti_static != bod_j.anti_static) ) )
				update_j = update_j and (not bod_i.anti_static or (bod_j.anti_static and (bod_i.anti_static != bod_j.anti_static) ) )

				if not update_i and not update_j:
					pass # add nothing
				else:
					x = self.central_force( xs[j], xs[i], bod_j, bod_i )

					if update_i:   
						for k in range(0,d):   out[i*d+k] += x[k]
					if update_j:   
						for k in range(0,d):   out[j*d+k] -= x[k]

		# Now, need to flatten the dp_dt arrays
		return out


	def dp_dt_fast(self, t, xs, ps):
		pass # TODO



	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	def solve_Nbody(self, t_fin, numeric_solver, out="xp"):

		x0s = self.system.x0s
		v0s = self.system.v0s
		N = self.system.N
		d = self.system.d

		x0s_flat = flatten_fast(x0s)
		v0s_flat = flatten_fast(v0s)
		p0s_flat = self.v2p(0, x0s_flat, v0s_flat)

		xs_flat,ps_flat,t = self.solve(t_fin, x0s_flat, p0s_flat, numeric_solver)

		vs_flat = self.p2v(t,xs_flat,ps_flat)

		xs = bundle(xs_flat, N,d)
		vs = bundle(vs_flat, N,d)
		ps = bundle(ps_flat, N,d)

		if out=="xp":
			return xs,ps,t
		else:
			return xs,vs,t

