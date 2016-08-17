import os
from sc_check import *

source_file = '/home/leonel/Dropbox/Work/PythonExamples/Source_Interface/sourcefiles_given/1200MeV-distribution.txt'


source = Source_File(source_file)

source.set_magnitudes(default_magnitudes)
source.set_units(default_units)

source.import_file(skip_header=5)

# source.save_standard_sourcefile('std_srcfile.txt')

# todo bien hasta aqui
print source.check_cosines()

ax = dircosines_surf(source)

plt.show()
