#ifndef __SERVER_H
#define __SERVER_H

#include "ipcstructs.h"
#include "dmx.h"

typedef struct {
    IPCData * ipcdata;
    SoundInfo * soundinfo;
    DMXPanelCollection * panel;
    int shmid;
    int semid;
} ServerInfo;

#endif
