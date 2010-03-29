

try:
    from csexp import *
    SEXP_VERSION = "C Module"
except ImportError:
    from pysexp import *
    SEXP_VERSION = "Pure Python"
