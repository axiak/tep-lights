CC = gcc
CCFLAGS = -Wall -std=c99 -pedantic -D_SVID_SOURCE=1 -I../inc

simple: simpleplugin.c ../src/plugin.c ../src/plugin.h
	$(CC) -g -I../src -O2 $(CCFLAGS) simpleplugin.c ../src/ipcstructs.c ../src/plugin.c ../src/dmx.c -o simple

geomtest: geomtest.c
	$(CC) -g -I../src -O2 $(CCFLAGS) geomtest.c ../src/geom.c ../src/ipcstructs.c ../src/plugin.c ../src/dmx.c -o geomtest

sweep: sweep.c
	$(CC) -g -I../src -O2 $(CCFLAGS) sweep.c ../src/geom.c ../src/ipcstructs.c ../src/plugin.c ../src/dmx.c -o sweep

clean:
	rm -f simple
