/* Header file for effect utilities */
#ifndef __EFFECT_H
#define __EFFECT_H
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>

#include "ipcstructs.h"

typedef struct {
    IPCData * ipcdata;
    ClientInfo * info;
    SoundInfo * soundinfo;
    int shmid;
    unsigned long old_frame_counter;
    ColorLayer * layer;
} LocalData;

LocalData * plugin_register(char * filename, int id);
int serverdata_update(LocalData * data);
void serverdata_destroy(LocalData * data);
void serverdata_commitlayer(LocalData * data);


#endif
