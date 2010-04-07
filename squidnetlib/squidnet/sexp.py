

try:
    from scexp import *
    SEXP_VERSION = "C Module"
except ImportError:
    try:
        from csexp import *
        SEXP_VERSION = "Cython Module"
    except ImportError:
        from pysexp import *
        SEXP_VERSION = "Pure Python"
