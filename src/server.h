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

ServerInfo * new_serverenvironment();

void destroy_serverenvironment(ServerInfo * info);

void destroy_shmdata(void);
#endif
