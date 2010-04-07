from distutils.core import setup
from distutils.extension import Extension


import os
import glob
import sys

TRY_CYTHON = True
cmdclass = {}
ext_modules = []
TRY_BUILD = True

if '--no-cython' in sys.argv:
    TRY_CYTHON = False
    sys.argv.remove('--no-cython')

if '--no-build' in sys.argv:
    TRY_BUILD = False
    sys.argv.remove('--no-build')


if TRY_CYTHON:
    try:
        from Cython.Distutils import build_ext
        cmdclass = {'build_ext': build_ext}
        ext_modules = [Extension("squidnet.csexp", ["squidnet/csexp.pyx"])]
    except ImportError:
        pass
    else:
        try:
            os.unlink(os.path.join(os.path.dirname(__file__),
                                   'squidnet',
                                   'csexp.c'))
        except OSError:
            pass


if not ext_modules:
    print "Not using Cython for fast sexp module.".upper()
    if TRY_BUILD:
        ext_modules = [Extension("squidnet.csexp", ["squidnet/csexp.c"])]
else:
    print "USING CYTHON"

py_modules = [x.split('.')[0] for x in 
              glob.glob(os.path.join(os.path.dirname(__file__), 'squidnet', '*.py'))]

version = __import__('squidnet').VERSION
versionstring = '.'.join(map(str, version))
authors = __import__('squidnet').AUTHORS
emails = __import__('squidnet').EMAILS
authorstring = ', '.join(authors)
emailstring = ', '.join(emails)
setup(
  name = 'squidnet',
  cmdclass = cmdclass,
  version = versionstring,
  author = authorstring,
  author_email = emailstring,
  license = "GPL Version 3",
  description = "SquidNet interface",
  ext_modules = ext_modules,
  py_modules = py_modules,
  classifiers = [
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Cython',
        'Programming Language :: Python',
        'Topic :: Communications',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Networking',
        ],
)
