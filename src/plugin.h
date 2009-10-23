/* Header file for effect utilities */
#ifndef __EFFECT_H
#define __EFFECT_H
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>

#include "ipcstructs.h"


typedef struct {
    SoundInfo * soundinfo;
    int shmid;
    key_t server_key;
    unsigned long old_frame_counter;
} ServerData;

ServerData * serverdata_new(char * server_name);
int serverdata_update(ServerData * data);
void serverdata_destroy(ServerData * data);

typedef struct {
    ColorLayer * layer;
    ColorLayer * _server_layer;
    int semid;
    int shmid;
} LayerInfo;

LayerInfo * layerinfo_create(char * progname, char * server_name);
int layerinfo_commit(LayerInfo * layer);
void layerinfo_destroy(LayerInfo * layer);

#endif
