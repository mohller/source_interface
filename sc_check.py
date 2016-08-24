import numpy as np
import re
import sys
import pint

import scipy.stats as st

un = pint.UnitRegistry()

# Self Consistency Check for Source Files
# .... check consistency of external source files
#  Author: Leonel Morejon
#  Date: 29/07/2016


epsilon = 1e-200 # tolerance for cosines square sum

# default_magnitudes = ('pid','x','y','z','tx','ty','tz','E','w')
default_magnitudes = ('x','y','z','tx','ty','tz','E','w')
default_units = ('cm',)*3 + ('dimensionless',)*3 + ('GeV','dimensionless')
# default_units = {'x':'cm',   'y':'cm',   'z':'cm',
				# 'tx':'adim','ty':'adim','tz':'adim',
				 # 'E':'GeV',  'w':'adim'}




def guess_sdist(pos_dict):
	'''Test function to determine the spatial distribution
		of the source. It takes a dictionary with the same
		structure as data in the source object, that contains
		only the 'x','y','z' values
	'''
	for k in pos_dict:
		if np.all(pos_dict[k] == pos_dict[k][0]):
			pos_dict[k] = pos_dict[k][0]

	return pos_dict




#### ------- Class for source files
class Source_File(object):
	"""Placeholder class for external source files
	   provided and by external codes.
	"""
	def __init__(self, *args, **kwargs):
		super(Source_File, self).__init__()
		fname = args[0]
		self.filename = fname
		self.data = {}
		self.magnitudes = ()
		self.units = ()

		# Initialize description dictionary ...
		self.description = {'parID' : 'unknown',
							'sdist' : 'point',
							'pdist' : 'pencilbeam',
							'edist' : 'monoenergetic'}
		# ... and assign given values
		for k in self.description: 
			if k in kwargs:
				self.description[k] = kwargs[k];


		# distribution functions: uniform by default
		s_dist = st.uniform() # spatial distribution function 
		p_dist = st.uniform() # direction distribution function
		e_dist = st.uniform() # energy distribution function

	def import_file(self, *args, **kwargs):
		''' Assuming the file contains a set of columns. 
			This is just a wrapper for genfromtxt with some post 
			processing of the sourcefile data. In other words
			it accepts all the same arguments as genfromtxt
			(see http://docs.scipy.org/doc/numpy/reference/generated/numpy.genfromtxt.html) 
		'''
		matrix = np.genfromtxt(self.filename, *args, **kwargs)

		matrix = matrix.transpose() # to have columns into rows

		for mag,u,vals in zip(self.magnitudes, self.units, matrix):
			unit = un.Quantity(u) # choose the units from un
			self.data[mag] = vals * unit

		# call methods to convert from non-standard to standard magnitudes
		if set( ('Bx','By','Bz') ).issubset(default_magnitudes):
			B = np.sqrt(self.data['Bx']**2 + self.data['By']**2 + self.data['Bz']**2)
			
			sef.data['tx'] = self.data['Bx'] / B
			sef.data['ty'] = self.data['By'] / B
			sef.data['tz'] = self.data['Bz'] / B

			self.check_cosines()

		# check consistency between magitudes, units and the 
		# columns in the file imported

		# call methods to set source description parameters: e.g. point, monochromatic, etc


	def set_magnitudes(self, magnitudes):
		# set a list of magnitudes which refer to the columns in the file
		self.magnitudes = magnitudes

	def set_units(self, unit_labels):
		# set a list of units which refer to the columns in the file
		# these will be used by the self consistency check
		self.units = [un.Quantity(u) for u in unit_labels]

	def check_cosines(self):
		# checking that direction cosines
		# if ok returns 0, otherwise returns 1

		return_value = 0

		if set( ('tx','ty','tz') ).issubset(default_magnitudes):

			tx = self.data['tx'].magnitude
			ty = self.data['ty'].magnitude
			tz = self.data['tz'].magnitude

			s = tx**2+ty**2+tz**2
			
			if np.any( s > 1-epsilon ):
				return_value = np.where(s > 1-epsilon)
				print "Warning: Not normalized cosines!"
		else:
			return_value = 1
			print "Error: Some or all director cosines are undefined."

		return return_value

	def smear_positions(self,fixed=('z',)):
		'''Smear the cosines leaving fixed the components along the
		direction given (by default 'z')
		'''
		x = sourcefileobject.data['tx'].magnitude
		y = sourcefileobject.data['ty'].magnitude
		z = sourcefileobject.data['tz'].magnitude

		grid_x, grid_y = np.mgrid[min(x):max(x):100j, min(y):max(y):100j]

		grid_z = griddata((x, y), z, (grid_x, grid_y), method='cubic')

	def renorm_weight(self,norm):
		if 'w' in self.magnitudes:
			self.data['w'] *= 1./norm
		else:
			print "Error: No weight values defined"


	def save_standard_sourcefile(self,fname):
		mag = default_magnitudes[0]
		export_array = self.data[mag].magnitude

		for mag in default_magnitudes[1:]:
			if mag in self.magnitudes:
				export_array = np.vstack( [export_array, self.data[mag].magnitude] )

		# this below writes in fortran readable format
		# the + sign in front of positive numbers could be problematic
		# in that case, a simple function using re to change '   +' into '    ' should work
		np.savetxt('source_file.dat', export_array, fmt="%+15.8e", delimiter='   ')
	

