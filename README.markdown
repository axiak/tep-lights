# tep-lights

The code in here is used to control lights and other things
within tEp. As of writing, there are three distinct directories:

## pydmx

`pydmx` contains the python code to manipulate the dining room LED
wall. Since it's in python, it's too slow to do complicated interactions
with audio, so that's what cdmx is developed for. For examples of what
you can do in pydmx, look at tron.py and shimmering.py.

## cdmx

This directory contains the C code in order to create a audio-aware
overlay system. The architecture is that one can write a plugin in
the plugins directory, and then run everything. You can test it
out by running audiotestserver first. This code requires libsdl,
libjack, and libfftw3 in order to compile.

## squidnet

This directory contains the code necessary to power the servers
and clients of SquidNet. The squidnet library requires the python
development headers in order to compile.