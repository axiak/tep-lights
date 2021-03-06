=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
SFSEXP: Small Fast S-Expression Library
http://sexpr.sourceforge.net/

Matt Sottile (matt@cs.uoregon.edu)
University of Oregon
Department of Computer and Information Science
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

1. BUILDING

(Attention Windows Users: If you are using cygwin, this section applies
as cygwin looks pretty much like unix for compilation.  Visual Studio
users see the note at the end and look inside the win32 directory.)

First, you need to run autoconf.

	% ./configure

To build, do this:

	% make

What comes out is a library called "libsexp.a".  That's it.  It may
be possible that whatever platform you're on may link libraries in a
weird way, so you might have to tweak the makefile.

Successfully tested under:
   RedHat Linux (Intel and Alpha), MacOS X 10.1.x -> 10.4.x,
   Suse Linux 9.1 (Intel and AMD), Debian Sarge, Ubuntu 6.10

Should work on:
   Anything with a standard C compiler

If you look at the makefiles, you'll see a couple of additional build
targets -- debug and mallocdebug.  Debug turns on anything hiding in #ifdef
_DEBUG_ blocks and compiles the code with -g so GDB can work.

If you want the docs, make sure you have doxygen installed and that the
DOXYGEN variable in the Makefile.in in this directory points at the right
place.  Rerun autoconf to regenerate the makefiles, and then type:

	% make doc

If all is well, you should get documentation.  If not, try running it by hand.
If that still fails, just use the docs from the web.  The documentation here
changes so infrequently that users generating it themselves is not a huge
concern on my end.

2. USING

In any code that wants to use this, just include "sexp.h".  That contains
the one data structure, enumeration, and five functions for manipulating
and parsing strings and s-expressions.  To compile, just do something like
this:

	% cc -I/path/to/sexp/include -L/path/to/sexp/library \
		-o foo  foo.o -lsexp

3. MORE INFO

For additions, bug fixes, complaints, etc., email : matt@lanl.gov
For legal mumbo-jumbo, look at "LICENSE" in this directory.  

4. SMALLER?

It's shorter than a few similar libraries I found on the net that were
IMHO, excessively complex and difficult to understant.  An s-expression
is composed of atoms, or other s-expressions - period.  How people can
turn that into a complicated mess is BEYOND me...

5. CREDITS

The library is by Matt Sottile.  Steve James of Linux Labs has contributed
bug fixes and features while developing for the related Supermon project.
Sung-Eun Choi and Paul Ruth have contributed many bug reports as the library
has grown.  Erik Hendriks contributed the malloc debugging tools now used
when building with the -D_DEBUG_MALLOCS_ option.  Brad Green contributed
code (in win32/) and testing for the Windows Visual Studio build target.

6. WINDOWS USERS

Please look in the win32/ subdirectory.  Included in there is one source
file, some 
