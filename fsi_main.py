import numpy as np
import re
import sys
# Source Interface
# .... input complex sources in a simple way
#  Author: Leonel Morejon
#  Date: 28/07/2016

class Generic_Interruption(Exception):
	"""A Generic Interruption for the functions..."""
	pass		


def particle_id(arg_id=7):
	''' Returns a particle id based on the arg_idument. 
		Default value is 7 ('gamma')
		It can interpret different inputs, like 'e', 'electron' for electrons,
		or 'gamma', 'gammas', 'phtons', 7, for photons, etc.
		Example:
		  particle('e') -> 7
		  particle('electron') -> 7
		  particle('photons') -> 7
		  particle('p') -> 
	'''

	if   arg_id in ('p', 'proton', 1): 			pid = 1;
	elif arg_id in ('e', 'electron', 'e-', 3):		pid = 3;
	elif arg_id in ('e+', 'positron', 4):			pid = 4;
	elif arg_id in ('g', 'gamma', 'photon', 7):	pid = 7;
	elif arg_id in ('n', 'neutron', 8): 			pid = 8;
	else:		
		pid = None
		print "Error: Particle not identified..."
		sys.exit()
		
	return pid

def test_particle_id():
	print particle_id('electron') == 3 
	# print particle_id('noparticle') == None # Should stop with error; tested and working properly 
	print particle_id('gamma') == 7
	print particle_id('photon') == 7
	print particle_id('proton') == 1


def sdist(dimmension='point', pos=[0,0,0], **kwargs):
	''' Returns a distribution for the spatial extension of the source.
		Default value is point source ('point') located in x=0,y=0,z=0
		It can interpret different inputs, like 'point', (3,4,5) as (x,y,z) position of source,
		or 'surface' and 'sphere' to get a source emmiting from a sphere's surface,
		or 'volume' and 'sphere' to get a source emmiting from a sphere's volume, etc.
		The parameters are structured as follows:
		  
		  dimmension: Any of value ('point', 'surface', 'volume')
		  
		  stype: Any of value ('plane', 'cylinder', 'sphere','quadratic')

		Example:
		  sdist('point', pos=(10,-2,30)) -> (10,-2,30)
		  provide further examples....
	'''
	
	# !!! It needs to be defined what will be the output of this function in general
	# !!! For the moment returns a dictionary of parameters

	if dimmension not in ('point', 'surface', 'volume'):
		
		# implement smart recognition for incomplete or mistyped arguments

		print "Error: Unknown value for dimmension. Choose between ('point','surface','volume')" \
			  " or leave it unset to use the default value ('point')."
		sys.exit ()

	elif dimmension == 'point':	

		# select a dimmension based on provided kwargs (when dimmension not provided)

		parameters = {'pos':pos};

	elif dimmension == 'surface':
		# determine stype if given
		if 'stype' not in kwargs.keys():
			print "Error: argument 'stype' not given. Choose between ('plane')"
			sys.exit()
		if kwargs['stype'] == 'plane':			
			if 'nvector' not in kwargs.keys(): 
				nvector = [0,0,1]
			else:
				nvector = kwargs['nvector']				
			parameters = {'pos':pos, 'nvector':nvector}
		else:
			print "Sorry, stype='{0}' not implemented yet.".format(kwargs['stype'])
			sys.exit()

	elif dimmension == 'volume':
		print "Sorry, dimmension='{0}' not implemented yet.".format(dimmension)
		sys.exit()

	return parameters

def test_sdist():
	# print sdist(dimmension='wrong_value') # Should stop with error; tested and working properly 
	print sdist()
	print sdist(dimmension='surface', stype='plane')
	print sdist(dimmension='surface', stype='sphere')
	print sdist(dimmension='volume')



test_particle_id()
test_sdist()