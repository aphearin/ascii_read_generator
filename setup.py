from distutils.core import setup
from Cython.Build import cythonize

setup(ext_modules=cythonize('cythonize_array_fill.pyx'))

# compile instructions:
# python setup.py build_ext --inplace
