import numpy as np
import re
import sys
# Source Interface
# .... input complex sources in a simple way
#  Author: Leonel Morejon
#  Date: 28/07/2016


default_dimmensions = ('point', 'surface', 'volume', 'custom')

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

	if   arg_id in ('p', 'proton', 1): 				pid = 1;
	elif arg_id in ('e', 'electron', 'e-', 3):		pid = 3;
	elif arg_id in ('e+', 'positron', 4):			pid = 4;
	elif arg_id in ('g', 'gamma', 'photon', 7):		pid = 7;
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
		It can interpret different inputs, like 'point', (3,4,5) as (x,y,z) position of source
		in cm; or 'surface' and 'sphere' to get a source emmiting from a sphere's surface,
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

	if dimmension not in default_dimmensions:
		
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


def pdist(dimmension='pencilbeam', dir=[0,0,1], **kwargs):
	''' Returns a distribution for the momenta of the source.
		Default value is unidirectional ('pencil') oriented to tx=0,ty=0,tz=1
		It can interpret different inputs, like 'isotropic', 'x','y','z' as orientations.
		It can also take a matrix of shape (n x 3) of vectors representing the momenta spectrum 
		The parameters are structured as follows:
		  
		  dimmension: Any of value ('pencilbeam', 'isotropic')
		  
		  ptype: Any of value ('gaussian', 'custom')

		Example:
		  pdist('point', dir=(-1,0,0)) -> (-1,0,0)
		  pdist('dirint', dir=(-1,0,0)) -> (-1,0,0)
		  provide further examples....
	'''
	
	# !!! It needs to be defined what will be the output of this function in general
	# !!! For the moment returns a dictionary of parameters

	if dimmension not in ('pencilbeam', 'isotropic', 'custom'):
		
		# implement smart recognition for incomplete or mistyped arguments

		print "Error: Unknown value for dimmension. Choose between ('pencilbeam','isotropic')" \
			  " or leave it unset to use the default value ('pencilbeam')."
		sys.exit ()

	elif dimmension == 'pencilbeam':

		# select a dimmension based on provided kwargs (when dimmension not provided)

		parameters = {'dimmension':dimmension, 'dir':dir};

	elif dimmension == 'isotropic':

		parameters = {'dimmension':dimmension};

	elif dimmension == 'custom':
		print "Sorry, dimmension='{0}' not implemented yet.".format(dimmension)
		sys.exit()

	return parameters

def test_pdist():
	# print sdist(dimmension='wrong_value') # Should stop with error; tested and working properly 
	print pdist()
	print pdist(dimmension='pencilbeam', dir=[0,0,-1])
	print pdist(dimmension='isotropic')
	print pdist(dimmension='custom')


def edist(etype='monoenergetic', kinetic=True, mean=1e-3, width=0, **kwargs):
	''' Returns a distribution for the energy of the source.
		Default value is a monoenergetic source ('monoenergetic') of kinetic energy ('kinetic')
		and of energy 1MeV.
		It can interpret different inputs, like 'flat', 'gaussian', or even SymPy expressions.
		The parameters are structured as follows:
		  
		  etype: Any of value ('monoenergetic', 'flat', 'gaussian', 'function', 'data')
		  
		  kinetic: True or False for kinetic energy vs total energy. By default is True

		  mean: The mean value of energy in GeV. By default 1MeV

		  width: The mean width of the function. Relevant for 'flat' and 'gaussian' types.
		         By default is 0.

		Examples:

		  edist() -> {'etype':'monoenergetic', 'kinetic':True, 'mean':1e-3, 'width':0}

		  edist(etype='flat', width=5e-4) -> {'etype':'flat', 'kinetic':True, 'mean':1e-3, 'width':5e-4}

		  provide further examples....
	'''
	
	# !!! It needs to be defined what will be the output of this function in general
	# !!! For the moment returns a dictionary of parameters

	if etype not in ('monoenergetic', 'flat', 'gaussian', 'function', 'data'):
		
		# implement smart recognition for incomplete or mistyped arguments

		print "Error: Unknown value for etype. Choose between ('monoenergetic', 'flat',"\
			  " 'gaussian', 'function', 'data') or leave it unset to use the default value ('point')."
		sys.exit ()

	elif etype in ('monoenergetic', 'flat'):	

		parameters = {'etype':etype, 'kinetic':kinetic, 'mean':mean, 'width':width}

	elif etype == 'gaussian':
		# determine sigma if given
		if 'sigma' not in kwargs.keys():
			print "Warning: Argument 'sigma' not given, mean={0} taken instead".format(mean)
			sigma = mean
		
		parameters = {'etype':etype, 'kinetic':kinetic, 'mean':mean, 'sigma':sigma}			

	elif etype in ('function', 'data'):
		print "Sorry, etype='{0}' not implemented yet.".format(etype)
		sys.exit()

	return parameters

def test_edist():
	print edist()
	print edist(etype='monoenergetic')
	print edist(etype='flat', mean=1)
	print edist(etype='function')
	print edist(etype='data')
	pass



test_particle_id()
# test_sdist()
# test_pdist()
test_edist()