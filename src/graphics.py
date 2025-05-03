import numpy as np

class Graphics:
	def __init__(self, dt=None, origin=None, trail_len=-1, max_plt_radius=np.inf, equal_aspect_ratio=True, plt_ham_error=True):
		self.dt = dt
		self.origin = origin
		self.trail_len = trail_len
		self.max_plt_radius = max_plt_radius
		self.equal_aspect_ratio = equal_aspect_ratio
		self.plt_ham_error = plt_ham_error