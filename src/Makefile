CC = gcc
CCFLAGS = -Wall -std=c99 -pedantic -D_SVID_SOURCE=1

etest: effect.c effect.h ipcstructs.h
	$(CC) -g -DEFFECTTEST $(CCFLAGS) effect.c -o etest
dmxtest: dmx.c dmx.h
	$(CC) -g -DDMX_TEST $(CCFLAGS) dmx.c -o dmxtest

clean:
	rm -f dmxtest etest
