import numpy as np
import matplotlib.pyplot as plt
import sys
import time

import src.vector as vector
import src.arrays as arr

import src.system.system as system
import src.system.body as body
import src.system.read_system as read_system
import src.system.write_system as write_system

from animate.animate_2d import animate_2d_orbits, animate_2d_plots
from animate.interpolate import interpolate_timestep





#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
TODOS:
 - electrostatics
 - clean up "potential data" code & Object
 - source terms (ie static bodies w/ mass and charge but do not evolve dynamically)


 Divide code up more into three stages
 - pre process
 - simulation
 - post process
"""



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
JSON Key words meaning

dt = time step in the animation or writing to file. This is not the simulation time steo

max dt = the maximum timestep used in the Kunge-Kutta Simulation


frame = COM, zero, or the name of a body [ie frame of reference]

powerlaw = force goes as 1/r^k
"""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

input_file = "system-1.json"
output_dir = "test/"

show_animation = True
write_data = False
overwrite_data = False


if len(sys.argv) > 1:
	input_file = sys.argv[1]

if len(sys.argv) > 2:
	write_data = True
	output_dir = sys.argv[2] + "/"

if len(sys.argv) > 3:
	overwrite_data = True



#####   Data relevant only to plotting

## QUESTION:  What does 'interval' actually mean ?
#             and how can I make the plotting consistent if I chnge tfin & dt ?

#trail_len = 100
interval = 50
plot_hamiltonian = True
plt_error = False


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

t_fin, sys_data, physics, solver, visual_data = read_system.read_json( input_file )


### preprocess data

# check that names are unique.

# TODO


# find where the origin should be

origin_is_com = False   # don't centre origin to be centre of mass
origin_body_index  = -1  # (>=0) index of bodies from list of bodies

o_name = visual_data.origin
if type(o_name) == str:
	if o_name.upper() == "COM":
		origin_is_com = True

	else:
		for i in range(0, len(sys_data.bodies)):
			bd_name = sys_data.bodies[i].name

			if bd_name == o_name:
				origin_body_index = i
				break

		if origin_body_index < 0 and o_name.upper() != "ZERO":
			print("WARNING: Origin must be a body name, 'COM', or 'ZERO'. Not: {0}".format( o_name ))




#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# SIMULATE THE DYNAMICS
t_start = time.time()

Xs,Ps,t = physics.solve_Nbody( t_fin, solver, out="xp" )

t_end = time.time()

print("Simulation complete: elapsed time = {0:.3f}s".format(t_end-t_start))
tf = t[-1]
if tf < t_fin:
	print("WARNING:  Final simulation time: {0:.3f}\n          Expected time: {1:.3f}".format(t[-1], t_fin))


#####   Now analyse / plot / write data
N,d=sys_data.N, sys_data.d


# compute Hamiltonian
H = physics.hamiltonian_NBody( t, Xs, Ps )

H0 = physics.initial_hamiltonian()


# compute the error of the difference between computed & expected 
H_err = H-H0


#### FRAME OF MOTION

# recentre all of the orbits about some (dynamical) origin
XO = vector.zeroes( len(t) )  # XO = origin

if origin_is_com:
	# compute the Centre of Mass
	XO = body.centre_of_mass(sys_data.bodies,*Xs)
elif origin_body_index >= 0:
	XO = Xs[ origin_body_index ]


# CONVERT TO shifted frame
Xs_O = vector.subtract(XO, *Xs)



#### SMOOTH OUT AND EQUALISE TIME STEPS

### interpolate for constant timestep
Xs_O_interp, t_interp = interpolate_timestep( Xs_O, t, dt=visual_data.dt )


H_interp, _ = interpolate_timestep( H, t, dt=visual_data.dt )
H_err_interp, _ = interpolate_timestep( H_err, t, dt=visual_data.dt )


# Extract x & y components
xs_O_interp = [ Xs_O_interp[i][0] for i in range(0,N) ]
ys_O_interp = [ Xs_O_interp[i][1] for i in range(0,N) ]



### ANIMATE AND/OR WRITE DATA
colours = [ body.colour for body in sys_data.bodies ]


### plot the Hamiltonian.

if plt_error:
	plt.figure()
	plt.plot(t_interp,H_err_interp)
	plt.title("Error in Hamiltonian")
	plt.xlabel("time")
	plt.ylabel("H - H0")



if show_animation:

	### set limits
	x_min = min( [ min(xs_O_interp[i]) for i in range(0,len(xs_O_interp)) ] ) * 1.1
	x_max = max( [ max(xs_O_interp[i]) for i in range(0,len(xs_O_interp)) ] ) * 1.1

	y_min = min( [ min(ys_O_interp[i]) for i in range(0,len(xs_O_interp)) ] ) * 1.1
	y_max = max( [ max(ys_O_interp[i]) for i in range(0,len(xs_O_interp)) ] ) * 1.1

	if visual_data.equal_aspect_ratio:
		if x_min < y_min:  y_min = x_min
		else:              x_min = y_min
		if x_max > y_max:  y_max = x_max
		else:              x_max = y_max

	R = visual_data.max_plt_radius

	xlim = [ min(max(-R, x_min), (x_min-x_max)*0.1), max(min(R, x_max), (x_max-x_min)*0.1) ]
	ylim = [ min(max(-R, y_min), (y_min-y_max)*0.1), max(min(R, y_max), (y_max-y_min)*0.1) ]

	#####

	anim = animate_2d_orbits(xs_O_interp, ys_O_interp, colours, interval=interval, trail_len=visual_data.trail_len, xlim=xlim, ylim=ylim)

	if visual_data.plt_ham_error:
		ham_anim = animate_2d_plots(t_interp, H_err_interp, colours=['blue'], interval=interval, trail_len=visual_data.trail_len, xlabel="time", ylabel="$H-H(0)$", title="Error in Hamiltonian")

	plt.show()


if write_data:
	write_system.write_dynamics_dir(output_dir, sim_data.bodies, t_interp, Xs_O_interp, skip_lines=0, overwrite=overwrite_data)





