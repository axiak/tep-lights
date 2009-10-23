CC = gcc
CCFLAGS = -Wall -std=c99 -pedantic -D_SVID_SOURCE=1
INCS = -I../inc

server: *c *h
	$(CC) $(INCS) -g $(CCFLAGS) *.c -o testserver

plugin: plugin.c plugin.h ipcstructs.h ipcstructs.c
	$(CC) $(INCS) -g -DEFFECTTEST $(CCFLAGS) plugin.c ipcstructs.c -o plugintest

dmxtest: dmx.c dmx.h
	$(CC) $(INCS) -g -DDMX_TEST $(CCFLAGS) dmx.c -o dmxtest

geom: geom.c
	$(CC) $(INCS) -g $(CCFLAGS) $(CC) geom.c -c


clean:
	rm -f dmxtest plugintest

