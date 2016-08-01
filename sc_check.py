import numpy as np
import re
import sys
import pint

un = pint.UnitRegistry()

# Self Consistency Check for Source Files
# .... check consistency of external source files
#  Author: Leonel Morejon
#  Date: 29/07/2016

default_magnitudes = ('x','y','z','tx','ty','tz','E','w')
default_magnitudes = ('cm','cm','cm','','','','GeV','w')
# default_units = {'x':'cm',   'y':'cm',   'z':'cm',
				# 'tx':'adim','ty':'adim','tz':'adim',
				 # 'E':'GeV',  'w':'adim'}

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

	def import_file(self, *args, **kwargs):
		# assuming the file contains a set of columns
		# this is just a wrapper for genfromtxt
		# with some post processing of the sourcefile data
		matrix = np.genfromtxt(self.filename, *args, **kwargs)
		self.ms = range(matrix.shape[1])

		# check consistency between magitudes, units and the 
		# columns in the file imported

		# for mag,un in zip(magnitudes,units):
		for i in range(matrix.shape[1]): # for each column
			unit = un.Quantity(self.units[i]) # choose the units from un
			magn = self.magnitudes[i]
			self.data[magn] = matrix[:,i] * unit

	def set_magnitudes(self, magnitudes):
		# set a list of magnitudes which refer to the columns in the file
		self.magnitudes = magnitudes

	def set_units(self, units):
		# set a list of units which refer to the columns in the file
		# these will be used by the self consistency check
		self.units = [un.Quantity(u) for u in units]

	def save_standard_sourcefile(self,fname):
		export_array = np.array()

		for mag in default_magnitudes:
			if mag in self.magnitudes:
				export_array = np.vstack( [export_array, self.data[mag]] )

		export_array.tofile('source_file.dat', sep="   ", format="%f15.8")

			pass
	