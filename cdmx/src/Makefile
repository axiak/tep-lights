CC = gcc
CCFLAGS = -Wall -pedantic -std=c99 -D_SVID_SOURCE=1 -D_POSIX_SOURCE
INCS = -I../inc -I.

jackserver: *c *h
	$(CC) $(INCS) -lfftw3 -ljack $(CCFLAGS) ipcstructs.c dmx.c server.c jackserver.c beat.c -o jackserver

paserver: *c *h
	$(CC) $(INCS) -lfftw3 -lpulse-simple $(CCFLAGS) ipcstructs.c dmx.c server.c paserver.c beat.c -o paserver

patestserver: *c *h
	$(CC) $(INCS) -lSDL -lfftw3 -lpulse-simple $(CCFLAGS) -DTESTDUMMY dmxdummy.c ipcstructs.c dmx.c server.c paserver.c beat.c -o patestserver

naserver: *c *h
	$(CC) $(INCS) -lfftw3 $(CCFLAGS) ipcstructs.c dmx.c server.c testserver.c beat.c -o naserver

natestserver: *c *h
	$(CC) $(INCS) -lSDL -lfftw3 $(CCFLAGS) -DTESTDUMMY dmxdummy.c ipcstructs.c dmx.c server.c testserver.c beat.c -o natestserver

pluginlib: *c *h
	$(CC) $(INCS) -shared -fPIC plugin.c ipcstructs.c dmx.c geom.c -o libdmxplugin.so

jacktestserver: *c *h
	$(CC) $(INCS) -lSDL -lfftw3 -ljack $(CCFLAGS) -DTESTDUMMY beat.c ipcstructs.c dmx.c server.c dmxdummy.c jackserver.c -o jacktestserver

clean:
	rm -f dmxtest plugintest jacktestserver jackserver server libdmxplugin.so paserver patestserver naserver natestserver

install:
	cp libdmxplugin.so /usr/lib/
	rm -rf /usr/include/cdmx
	mkdir /usr/include/cdmx
	cp *.h /usr/include/cdmx
