#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <sys/sem.h>

#include <sys/time.h>
#include <time.h>

#include <errno.h>

#include "plugin.h"


LocalData * plugin_register(char * filename, int id)
{
    key_t key;
    int shmid = -1;
    int numtries = 0;
    LocalData * data = (LocalData *)malloc(sizeof(LocalData));
    int semid;
    int pluginid;
    struct sembuf sembuffer;

    if (!data) {
        return NULL;
    }

    fprintf(stderr, "Looking for %d bytes\n", sizeof(IPCData));
    key = ftok(MAINSEMFILE, 'a');
    if (key < 0) {
        fprintf(stderr, "Error getting shmkey\n");
        free(data);
        return NULL;
    }
    printf("Key: %d\n", key);
    while (numtries < 5000 && shmid < 0) {
        shmid = shmget(key, sizeof(IPCData), 0666);
        if (shmid < 0) {
            fprintf(stderr, "Waiting for SHM to exist...%d\n", key);
            usleep(10000);
            numtries++;
        }
    }
    if (shmid < 0) {
        fprintf(stderr, "Could not get shm data.\n");
        free(data);
        return NULL;
    }

    data->ipcdata = (IPCData *)shmat(shmid, NULL, 0);
    data->soundinfo = &data->ipcdata->soundinfo;

    key = ftok(MAINSEMFILE, 'L');
    srand(strlen(filename) * filename[2]);
    while (1) {
        pluginid = ((int)(abs(rand() * 1000))) % MAXPLUGINS;
        int i = data->ipcdata->plugins[pluginid].id;
        printf("%d\n", i);
        if (i == id) {
            fprintf(stderr, "We are already running!\n");
        }
        if (!i) {
            data->ipcdata->plugins[pluginid].id = id;
            break;
        }
        usleep(100);
    }
    fprintf(stderr, "We are plugin %d\n", pluginid);
    if (data->ipcdata == (IPCData *)-1) {
        fprintf(stderr, "Could not attach shared memory.\n");
        return NULL;
    }
    return data;
}


int serverdata_update(LocalData * data)
/* Wait until we get new data from the server... */
{
    while (data->old_frame_counter <= data->soundinfo->frame_counter) {
        usleep(10000);
    }
    return 0;
}

void serverdata_destroy(LocalData * data)
{
    if (!data) {
        return;
    }
    if (data->soundinfo) {
        shmdt(data->soundinfo);
    }
    free(data);
}


#ifdef EFFECTTEST
int main(int argc, char **argv)
{
    
    LocalData * s = plugin_register(argv[0], 0);
    printf("Number: %u\n", s->soundinfo->frame_counter);
    /*LocalData * s = serverdata_new("/tmp/x");*/
    gets(stdin);
    serverdata_destroy(s);
    return 0;
}

#endif
