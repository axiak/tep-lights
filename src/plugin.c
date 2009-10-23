#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <sys/sem.h>

#include <sys/time.h>
#include <time.h>

#include "effect.h"


ServerData * serverdata_new(char * server_name)
{
    key_t key;
    int shmid;
    ServerData * data = (ServerData *)malloc(sizeof(ServerData));
    if (!data)
        return NULL;

    key = ftok(server_name, 0);
    if (key < 0) {
        fprintf(stderr, "Error getting shmkey\n");
        free(data);
        return NULL;
    }

    shmid = shmget(key, sizeof(SoundInfo), 0666);
    if (shmid < 0) {
        fprintf(stderr, "Could not get shm data.\n");
        free(data);
        return NULL;
    }

    data->soundinfo = (SoundInfo *)shmat(shmid, NULL, 0);
    if ((int)data->soundinfo <= 0) {
        fprintf(stderr, "Could not attach shared memory.\n");
        return NULL;
    }
    return data;
}


int serverdata_update(ServerData * data)
/* Wait until we get new data from the server... */
{
    while (data->old_frame_counter = data->soundinfo->frame_counter) {
        usleep(10000);
    }
    return 0;
}

void serverdata_destroy(ServerData * data)
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
    ServerData * s = serverdata_new("/tmp/x");
    return 0;


}

#endif
