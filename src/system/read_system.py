import json
from . import system, body, rnd_body
from ..simulation.physics import gravity, electrostatics, gravo_electro
from ..simulation import numeric_solver
from .. import graphics


bodies_key = 'bodies'

name_key = 'name'
mass_key = 'mass'
x0_key = 'x0'
v0_key = 'v0'
colour_key = 'colour'
charge_key = 'charge'

type_key = 'type'
num_key = 'num'
r_max_key = 'r max'
v_max_key = 'v max'
mass_var_key = 'mass var'
charge_var_key = 'charge var'


static_key = "static"
anti_static_key = "ghost"


#~~~~~~~~~~~~~~~~~~

dimension_key = 'dim'

t_fin_key = 'tfin'


## simulation
max_dt_key = 'max dt'
integration_method_key = 'method'
atol_key = 'atol'
rtol_key = 'rtol'


## physics
physics_key = 'physics'
gravity_key = 'gravity'
electrostatics_key = 'electrostatics'
grav_elec_key = 'gravo-electro'

grav_power_law_key = 'grav power law'
electro_power_law_key = 'electro power law'


## graphics
dt_key = 'dt'
trail_len_key = 'trail length'
max_plot_radius_key = 'max plot radius'
equal_aspect_ratio_key = 'equal ratio'
origin_key = 'frame'
plt_ham_error_key = 'plot Hamiltonian'



## body types
rnd_type = "random"
static_type = "static"



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def read_json(f_name:str):

	system_data = {}

	with open(f_name, 'r') as f:
		system_data = json.load(f)

	####  DATA VALUES
	t_fin = -1

	#~~~~~~~~~~~~~~~~~~
	# do essential data

	bodies = []
	N = 0
	d=0

	# get the number of dimensions of the system
	try:				d = system_data[ dimension_key ]
	except KeyError:	raise Exception( f_name + ' does not have number of dimensions "{0}"'.format(dimension_key) )

	# construct list of bodies
	try:				
		bodies_dict_ls = system_data[bodies_key]
		num = len(bodies_dict_ls)

		bodies = []
		for i in range(0,num):
			body = read_body( bodies_dict_ls[i], d )
			N += len(body)

			bodies += body

	except KeyError:	raise Exception("Improper json file format. Missing 'bodies'")


	try:				t_fin = system_data[ t_fin_key ]
	except KeyError:	raise Exception( f_name + ' does not have final time "{0}"'.format(t_fin_key) )


	###################
	#  construct the system data, simulation, and visualisation data

	# system of N bodies
	syst = system.System( bodies=bodies, dim=d )

	# simulation
	solver = numeric_solver.NumericIntegrator( ) 

	# visualisation
	syst_vis = graphics.Graphics( )


	# physics - ie the Equations of Motion to solve
	physics = read_physics( f_name, system_data, syst )


	#~~~~~~~~~~~~~~~~~~
	# non-essential data
	try:				syst_vis.dt = system_data[ dt_key ]
	except KeyError:	pass
	
	try:				syst_vis.origin = system_data[ origin_key ]
	except KeyError:	pass

	try:				syst_vis.trail_len = system_data[ trail_len_key ]
	except KeyError:	pass

	try:				syst_vis.max_plt_radius = system_data[ max_plot_radius_key ]
	except KeyError:	pass

	try:				syst_vis.equal_aspect_ratio = system_data[ equal_aspect_ratio_key ]
	except KeyError:	pass

	try:				syst_vis.plt_ham_error_key = system_data[ plt_ham_error_key ]
	except KeyError:	pass


	try:				solver.int_method = system_data[ integration_method_key ]
	except KeyError:	pass

	try:				solver.max_dt = system_data[ max_dt_key ]
	except KeyError: 
		print("WARNING: No maximum simulation timestep")
		#raise Exception( f_name + ' does not have simulation maximum timestep "{0}"'.format(max_dt_key) )

	try:				solver.atol = system_data[ atol_key ]
	except KeyError:	pass

	try:				solver.rtol = system_data[ rtol_key ]
	except KeyError:	pass


	return  t_fin, syst, physics, solver, syst_vis




#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

###  TODO:
#    check to make sure no bodies overlap in initial positions!

def read_body(json_dict, d):

	name = None
	mass = 1
	x0 = None
	v0 = None
	colour=None
	charge = 0

	anti_static = False
	static = False

	type = ""

	body_name_str = 'unnamed body'

	# try find name, if it exists
	try:
		name = json_dict[ name_key ]
		body_name_str = 'body "{0}"'.format(name)
	except KeyError:	pass

	#~~~~~~~~~~~~~~~~
	# ALL IS NOW NON-ESSENTIAL DATA
	try:				mass = json_dict[ mass_key ]
	#except KeyError:	raise Exception( body_name_str + ' does not have "{0}"'.format(mass_key) )
	except KeyError:	
		anti_static = True
		print('WARNING:  mass not specified for body "{0}". Use "{1}" key'.format(name, anti_static_key))


	#~~~~~~~~~~~~~~~~
	# do non-essential data

	try:				colour = json_dict[ colour_key ]
	except KeyError:	pass

	try:				charge = json_dict[ charge_key ]
	except KeyError:	pass


	##### Extra Information:

	try:				type = json_dict[ type_key ]
	except KeyError:	pass


	# non-interacting classes
	try:				static = json_dict[ static_key ]
	except KeyError:	pass

	try:				anti_static = json_dict[ anti_static_key ]
	except KeyError:	pass


	##### Modify reading for diferent body types
	if type.lower() == rnd_type:

		N = 0
		r_max = 0.0
		v_max = 0.0
		charge_var = 0.0
		mass_var = 0.0

		try:				N = json_dict[ num_key ]
		except KeyError:	Exception( body_name_str + ' does not have number of bodies "{0}"'.format(num_key) )
		try:				r_max = json_dict[ r_max_key ]
		except KeyError:	Exception( body_name_str + ' does not have maximum radius "{0}"'.format(r_max_key) )
		try:				v_max = json_dict[ v_max_key ]
		except KeyError:	Exception( body_name_str + ' does not have maximum velocity "{0}"'.format(v_max_key) )

		try:				mass_var = json_dict[ mass_var_key ]
		except KeyError:	pass
		try:				charge_var = json_dict[ charge_var_key ]
		except KeyError:	pass

		return rnd_body.generate_random_bodies(N=N, d=d, r_max=r_max, v_max=v_max, mass=mass, charge=charge, mass_var=mass_var, charge_var=charge_var, anti_static=anti_static, static=static, colour=colour)

	else:

		#~~~~~~~~~~~~~~~~
		# do essential data
		try:				x0 = json_dict[ x0_key ]
		except KeyError:	raise Exception( body_name_str + ' does not have initial conditions "{0}"'.format(x0_key) )

		try:				v0 = json_dict[ v0_key ]
		except KeyError:	raise Exception( body_name_str + ' does not have initial conditions "{0}"'.format(v0_key) )

		bd = body.Body(x0, v0, mass, colour, name=name, charge=charge, anti_static=anti_static, static=static)

		return [ bd ]








####################

def read_physics( f_name , system_data, syst ):
	"""
	X
	"""

	physics = None

	try:				
		physics_str = system_data[ physics_key ]

		if physics_str == gravity_key:
			physics = gravity.Gravity( syst )

			try:				physics.power_law = system_data[ grav_power_law_key ]
			except KeyError:	pass


		elif physics_str == electrostatics_key:
			physics = electrostatics.ElectroStatics( syst )

			try:				physics.power_law = system_data[ elec_power_law_key ]
			except KeyError:	pass


		elif physics_str == grav_elec_key:
			physics = gravo_electro.GravoElectro( syst )

			try:				physics.grav_power_law = system_data[ grav_power_law_key ]
			except KeyError:	pass
			try:				physics.electro_power_law = system_data[ electro_power_law_key ]
			except KeyError:	pass


		else:
			raise ValueError( 'The physics "{0}" (in {1}) is not implemented'.format(physics_str, f_name))

	except KeyError:	
		raise Exception( f_name + ' does not have physics "{0}"'.format(physics_key) )

	return physics

