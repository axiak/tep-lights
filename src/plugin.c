#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <sys/sem.h>

#include <sys/time.h>
#include <time.h>

#include "plugin.h"


LocalData * plugin_register(char * filename, int id)
{
    key_t key;
    int shmid = -1;
    int numtries = 0;
    LocalData * data = (LocalData *)malloc(sizeof(LocalData));

    if (!data) {
        return NULL;
    }

    fprintf(stderr, "Looking for %d bytes\n", sizeof(IPCData));
    key = ftok(MAINSEMFILE, 0);
    if (key < 0) {
        fprintf(stderr, "Error getting shmkey\n");
        free(data);
        return NULL;
    }
    printf("Key: %d\n", key);
    while (numtries < 500 && shmid < 0) {
        shmid = shmget(key, sizeof(IPCData), 0666);
        if (shmid < 0) {
            fprintf(stderr, "Waiting for SHM to exist...\n");
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

    if ((int)data->soundinfo <= 0) {
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
    
    LocalData * s = plugin_register(__FILE__, 0);
    /*LocalData * s = serverdata_new("/tmp/x");*/
    return 0;


}

#endif
