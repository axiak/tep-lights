CC = gcc
CCFLAGS = -Wall -std=c99 -pedantic -D_SVID_SOURCE=1
INCS = -I../inc -I.

audioserver: *c *h
	$(CC) $(INCS) -lfftw3 -ljack -g $(CCFLAGS) ipcstructs.c dmx.c server.c audioserver.c -o audioserver

server: *c *h
	$(CC) $(INCS) -g $(CCFLAGS) ipcstructs.c dmx.c testserver.c server.c -o testserver

plugin: plugin.c plugin.h ipcstructs.h ipcstructs.c geom
	$(CC) $(INCS) -g -DEFFECTTEST $(CCFLAGS) plugin.c ipcstructs.c -o plugintest

dmxtest: dmx.c dmx.h
	$(CC) $(INCS) -g -DDMX_TEST $(CCFLAGS) dmx.c -o dmxtest

geom: geom.c
	$(CC) $(INCS) -g $(CCFLAGS) geom.c -c

clean:
	rm -f dmxtest plugintest

