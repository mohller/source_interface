import os
from sc_check import *
from report import *

source_files = [
	'/home/leonel/Dropbox/Work/PythonExamples/Source_Interface/sourcefiles_given/1200MeV-distribution.txt',
	'/home/leonel/Dropbox/Work/PythonExamples/Source_Interface/sourcefiles_given/merged-left-X_sh1Sbb-X_sh2Sbb_y0.spectr'
	]

source_file = '/home/leonel/Dropbox/Work/PythonExamples/Source_Interface/sourcefiles_given/1200MeV-distribution.txt'


source = Source_File(source_file)

# source.set_magnitudes(default_magnitudes[1:]) # without the pid 
source.set_magnitudes(default_magnitudes)
source.set_units(default_units)

source.import_file(skip_header=5)

# source.save_standard_sourcefile('std_srcfile.txt')

print source.check_cosines()

ax = dircosines_surf(source)

plt.show()

# todo bien hasta aqui

print source.data['z']
res = guess_sdist( dict((k,source.data[k]) for k in source.data) )
print res['z']
