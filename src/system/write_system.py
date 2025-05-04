import os




def write_csv(f_name:str, data_dict, data_range, skip_lines:int=0, overwrite=False):
	"""
	"skip": how often to print lines, 
			e.g. skim=0 is print every line, skim=10 is every tenth line.
	"""

	f = None
	if overwrite:
		f = open(f_name, 'w')
	else:
		try:
			f = open(f_name, 'x')
		except FileExistsError:
			print( "Cannot write simulation data.  File '{0}' already exist.".format(f_name) )
			return

	try:
		keys = data_dict.keys()

		key_line = ""
		for key in keys:
			key_line += key + ","
		key_line = key_line[:-1] + "\n"
		f.write(key_line)

		for i in range(0, data_range):
			# if the line is not a skim line write OR last line

			if (i%(skip_lines+1) == 0) or (i+1==data_range):
				
				line = ""
				for key in keys:
					line += "{0:.3f},".format( data_dict[key][i] )
				line = line[:-1] + "\n"
				f.write(line)

	except Exception as err:
		f.close()
		raise err

	return



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def mk_data_dict(t, *Xs):

	data_dict = {}

	data_dict['t'] = t

	N = len(Xs)

	for n in range(0,N):
		d = len(Xs[n])

		for i in range(0,d):
			key_name = 'x{0}_{1}'.format(n+1,i+1) 
			if N == 1:
				key_name = 'x_{0}'.format(i+1) 

			data_dict[ key_name ] = Xs[n][i]

	return data_dict



def write_dynamics_csv(f_name:str, t, Xs, data_range=-1, skip_lines=0, overwrite=False):

	if data_range < 0:
		data_range = len(t)

	data_dict = mk_data_dict(t, *Xs)

	write_csv(f_name, data_dict, data_range, skip_lines=skip_lines, overwrite=overwrite)

	return




#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def write_dynamics_dir(dir_name:str, bodies, t, Xs, data_range=-1, skip_lines=0, overwrite=False):

	if data_range < 0:
		data_range = len(t)


	try:
		os.mkdir(dir_name)
	except FileExistsError:
		if overwrite:
			print("WARNING: directory '{0}' already exists - contents have been overwritten".format(dir_name))

	N = len(bodies)

	if len(bodies) != len(Xs):
		raise ValueError("Not enough bodies to print")

	for i in range(0,N):
		body_name = str(bodies[i].name)
		f_name = dir_name + body_name + ".csv"

		with open(f_name, "w") as f:
			data_dict = mk_data_dict(t, Xs[i])

			write_csv(f_name, data_dict, data_range, skip_lines=skip_lines, overwrite=overwrite)

	return



