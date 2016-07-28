import numpy as np
import re

# Source Interface
# .... input complex sources in a simple way
#  Author: Leonel Morejon
#  Date: 28/07/2016

def particle_id(arg=7):
	''' Returns a particle id based on the argument. 
		Default value is 7 ('gamma')
		It can interpret different inputs, like 'e', 'electron' for electrons,
		or 'gamma', 'gammas', 'phtons', 7, for photons, etc.
		Example:
		  particle('e') -> 7
		  particle('electron') -> 7
		  particle('photons') -> 7
		  particle('p') -> 
	'''

	if   arg in ('p', 'proton', 1): 			pid = 1;
	elif arg in ('e', 'electron', 'e-', 3):		pid = 3;
	elif arg in ('e+', 'positron', 4):			pid = 4;
	elif arg in ('g', 'gamma', 'photon', 7):	pid = 7;
	elif arg in ('n', 'neutron', 8): 			pid = 8;
	else:
		pid = None
		print "Error: Particle not identified..."
		
	return pid

def test_particle_id():
	print particle_id('electron') == 3 
	print particle_id('noparticle') == None
	print particle_id('gamma') == 7
	print particle_id('photon') == 7
	print particle_id('proton') == 1


def sdist():
	''' Returns a distribution.
		Default value is point source ('point')
		It can interpret different inputs, like 'point', (3,4,5) as (x,y,z) position of source, for electrons,
		or 'gamma', 'gammas', 'phtons', 7, for photons, etc.
		Example:
		  particle('e') -> 7
		  particle('electron') -> 7
		  particle('photons') -> 7
		  particle('p') -> 
	'''

	pass




test_particle_id()
	