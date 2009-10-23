CC = gcc
CCFLAGS = -Wall -std=c99 -pedantic -D_SVID_SOURCE=1

simple: simpleplugin.c
	$(CC) -g -I../src -O2 $(CCFLAGS) simpleplugin.c ../src/ipcstructs.c ../src/plugin.c ../src/dmx.c -o simple
