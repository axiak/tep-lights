import os

from distutils.core import setup
from distutils.extension import Extension

kwargs = {}
ext_modules = []
ext_files = {}

cdmx_src = os.path.join(os.path.dirname(__file__),
                        '..', 'cdmx', 'src')

try:
   from Cython.Distutils import build_ext
   print "Building from Cython"
   ext_files['dmx'] = ['src/dmx.pyx']
   kwargs['cmdclass'] = {'build_ext': build_ext}
except ImportError:
   ext_files['dmx'] = ['src/dmx.c']

ext_modules = [Extension("cydmx.dmx",
                         ext_files['dmx'],
                         libraries = ['dmxplugin'],
                         )]

setup(name = "cydmx",
      version = "0.0.1",
      description = "cDmx for python!",
      author = "Michael Axiak",
      author_email = "mike@axiak.net",
      ext_modules = ext_modules,
      py_modules = ['cydmx.__init__', 'cydmx.dmxwidget'],
      **kwargs)
