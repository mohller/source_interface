import numpy as np
import re
import sys

# Self Consistency Check for Source Files
# .... check consistency of external source files
#  Author: Leonel Morejon
#  Date: 29/07/2016

class Source_File(object):
	"""Placeholder class for external source files
	   provided and by external codes.
	"""
	def __init__(self, fname):
		super(Source_File, self).__init__()
		self.filename = fname
		self.import_file(fname)

	def import_file(self, filename):
		# assuming the file contains a set of columns
		matrix = genfromtxt()

		pass
		