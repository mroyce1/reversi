import numpy
from distutils.core import setup
from Cython.Build import cythonize
import Cython.Compiler.Options
Cython.Compiler.Options.annotate = True

setup(
    ext_modules=cythonize('compiled.pyx', annotate=True),
    include_dirs=[numpy.get_include()]
)