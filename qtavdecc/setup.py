'''
Created on Feb 9, 2015

@author: christoph
'''
from distutils.core import setup
from Cython.Build import cythonize

# setup(ext_modules = cythonize(
#            "_adp.pyx",                 # our Cython source
#            sources=["Rectangle.cpp"],  # additional source file(s)
#            language="c++",             # generate C++ code
#       ))


setup(
    name = "_avdecc_cython",
    ext_modules = cythonize('*.pyx'),
)