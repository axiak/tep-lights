from distutils.core import setup
from distutils.extension import Extension


import os
import glob
import sys

TRY_CYTHON = True
cmdclass = {}
ext_modules = []

if '--no-cython' in sys.argv:
    TRY_CYTHON = False
    sys.argv.remove('--no-cython')


if TRY_CYTHON:
    try:
        from Cython.Distutils import build_ext
        cmdclass = {'build_ext': build_ext}
        ext_modules = [Extension("squidnet.csexp", ["squidnet/csexp.pyx"])]
    except ImportError:
        pass


if not ext_modules:
    print "Not using Cython for fast sexp module.".upper()


py_modules = [x.split('.')[0] for x in 
              glob.glob(os.path.join(os.path.dirname(__file__), 'squidnet', '*.py'))]


setup(
  name = 'SquidNet protocol implementations',
  cmdclass = cmdclass,
  ext_modules = ext_modules,
  py_modules = py_modules,
)
