CC = gcc
CCFLAGS = -Wall -pedantic -std=c99 -D_SVID_SOURCE=1 -D_POSIX_SOURCE
INCS = -I../inc -I.

jackserver: *c *h
	$(CC) $(INCS) -lfftw3 -ljack $(CCFLAGS) ipcstructs.c dmx.c server.c jackserver.c beat.c -o jackserver

paserver: *c *h
	$(CC) $(INCS) -lfftw3 -lpulse-simple $(CCFLAGS) ipcstructs.c dmx.c server.c paserver.c beat.c -o paserver

patestserver: *c *h
	$(CC) $(INCS) -lSDL -lfftw3 -lpulse-simple $(CCFLAGS) -DTESTDUMMY dmxdummy.c ipcstructs.c dmx.c server.c paserver.c beat.c -o patestserver

pluginlib: *c *h
	$(CC) $(INCS) -shared -fPIC plugin.c ipcstructs.c dmx.c geom.c -o libdmxplugin.so

jacktestserver: *c *h
	$(CC) $(INCS) -lSDL -lfftw3 -ljack $(CCFLAGS) -DTESTDUMMY beat.c ipcstructs.c dmx.c server.c dmxdummy.c jackserver.c -o jacktestserver

server: *c *h
	$(CC) $(INCS) $(CCFLAGS) ipcstructs.c dmx.c testserver.c server.c -o testserver

plugin: plugin.c plugin.h ipcstructs.h ipcstructs.c geom
	$(CC) $(INCS) -DEFFECTTEST $(CCFLAGS) plugin.c ipcstructs.c -o plugintest

dmxtest: dmx.c dmx.h
	$(CC) $(INCS) -DDMX_TEST $(CCFLAGS) dmx.c -o dmxtest

dmxdummy: dmxdummy.c
	$(CC) $(INCS) -DDMXDUMMY -lSDL $(CCFLAGS) dmx.c dmxdummy.c -o dmxdummy

clean:
	rm -f dmxtest plugintest jacktestserver jackserver server libdmxplugin.so paserver patestserver

install:
	cp libdmxplugin.so /usr/lib/
	rm -rf /usr/include/cdmx
	mkdir /usr/include/cdmx
	cp *.h /usr/include/cdmx
