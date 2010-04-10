CC = gcc
CCFLAGS = -Wall -pedantic -std=c99 -D_SVID_SOURCE=1 -D_POSIX_SOURCE
INCS = -I../inc -I.

audioserver: *c *h
	$(CC) $(INCS) -lfftw3 -ljack $(CCFLAGS) ipcstructs.c dmx.c server.c audioserver.c -o audioserver

audiotestserver: *c *h
	$(CC) $(INCS) -lSDL -lfftw3 -ljack $(CCFLAGS) -DTESTDUMMY ipcstructs.c dmx.c server.c dmxdummy.c audioserver.c -o audiotestserver

server: *c *h
	$(CC) $(INCS) $(CCFLAGS) ipcstructs.c dmx.c testserver.c server.c -o testserver

plugin: plugin.c plugin.h ipcstructs.h ipcstructs.c geom
	$(CC) $(INCS) -DEFFECTTEST $(CCFLAGS) plugin.c ipcstructs.c -o plugintest

dmxtest: dmx.c dmx.h
	$(CC) $(INCS) -DDMX_TEST $(CCFLAGS) dmx.c -o dmxtest

dmxdummy: dmxdummy.c
	$(CC) $(INCS) -DDMXDUMMY -lSDL $(CCFLAGS) dmx.c dmxdummy.c -o dmxdummy

clean:
	rm -f dmxtest plugintest audiotestserver audioserver server

