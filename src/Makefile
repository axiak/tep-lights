CC = gcc
CCFLAGS = -Wall -std=c99 -pedantic -D_SVID_SOURCE=1

server: *c *h
	$(CC) -g $(CCFLAGS) *.c -o testserver


plugin: plugin.c plugin.h ipcstructs.h ipcstructs.c
	$(CC) -g -DEFFECTTEST $(CCFLAGS) plugin.c ipcstructs.c -o plugintest
dmxtest: dmx.c dmx.h
	$(CC) -g -DDMX_TEST $(CCFLAGS) dmx.c -o dmxtest

clean:
	rm -f dmxtest plugintest
