CC = gcc
CFLAGS = -I../src -O2 -lm -D_POSIX_SOURCE
CCFLAGS = -Wall -std=c99 -pedantic -D_SVID_SOURCE=1 -I../inc

% : %.c
	$(CC) $(CFLAGS) $(CCFLAGS) $< ../src/ipcstructs.c ../src/plugin.c ../src/dmx.c ../src/geom.c -o $@
