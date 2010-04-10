#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <sys/sem.h>
#include <signal.h>

#include <sys/time.h>
#include <time.h>

#include <libgen.h>

#include <errno.h>

#include "plugin.h"

void clientinfo_print(ClientInfo * info)
{
    int i, first = 1;
    printf("---------------\nPlugin Information\n");
    printf("  We are client number: %d; id: %d\n", info->id, info->idx);
    printf("  Our name is '%s'\n", info->name);
    printf("  Our current inputs: [");

    for (i = 0; i < MAXPLUGINS; i++) {
        if (i == info->idx) {
            continue;
        }
        if (info->input_plugins[i]) {
            if (!first) {
                printf(", ");
            }
            first = 0;
            printf("%d", i);
        }
    }
    printf("]\n-------------------\n");
}

LocalData * plugin_register(char * progfilename, int id)
{
    key_t key;
    pid_t pid = getpid();
    int shmid = -1;
    int numtries = 0;
    LocalData * data = (LocalData *)malloc(sizeof(LocalData));
    int semid;
    int pluginid;

    if (!data) {
        return NULL;
    }

    key = ftok(MAINSEMFILE, 'a');
    if (key < 0) {
        fprintf(stderr, "Error getting shmkey\n");
        free(data);
        return NULL;
    }
    while (numtries < 5000 && shmid < 0) {
        shmid = shmget(key, sizeof(IPCData), 0666);
        if (shmid < 0) {
            fprintf(stderr, "Waiting for SHM to exist...%d (%d)\n", key, sizeof(IPCData));
            usleep(10000);
            numtries++;
        }
    }
    if (shmid < 0) {
        fprintf(stderr, "Could not get shm data.\n");
        free(data);
        return NULL;
    }

    data->shmid = shmid;
    data->ipcdata = (IPCData *)shmat(shmid, NULL, 0);
    data->soundinfo = &data->ipcdata->soundinfo;
    data->old_frame_counter = 0;
    key = ftok(MAINSEMFILE, 'L');
    srand(strlen(progfilename) * progfilename[2]);
    while (1) {
        pluginid = ((int)(abs(rand() * 1000))) % MAXPLUGINS;
        int i = data->ipcdata->plugins[pluginid].id;
        if (i == id) {
            fprintf(stderr, "We are already running!\n");
        }
        if (!i || !is_client_running(&data->ipcdata->plugins[pluginid])) {
            data->ipcdata->plugins[pluginid].id = id;
            data->info = &data->ipcdata->plugins[pluginid];
            data->info->pid = pid;
            data->info->idx = pluginid;
            memset(data->info->input_plugins, 0, sizeof(data->info->input_plugins));
            break;
        }
        usleep(100);
    }
    if (data->ipcdata == (IPCData *)-1) {
        fprintf(stderr, "Could not attach shared memory.\n");
        return NULL;
    }
    printf("Got seat\n");

    key = ftok(progfilename, 'L');
    semid = semget(key, 10, 0666 | IPC_CREAT);
    data->info->semid = semid;
    memcpy(data->info->name, basename(progfilename), 10);

    data->layer = colorlayer_create();
    data->layer->height = PIXELHEIGHT;
    data->layer->width = PIXELWIDTH;

    printf("Committing layer..\n");
    serverdata_commitlayer(data);
    printf("DONE\n");

    clientinfo_print(data->info);

    return data;
}

void serverdata_commitlayer(LocalData * data)
/* Commit the local layer to the master */
{
    begin_lightread(data->info);
    memcpy(data->info->layer.pixels, data->layer->pixels, sizeof(data->layer->pixels));
    data->info->layer.width = data->layer->width;
    data->info->layer.height = data->layer->height;
    end_lightread(data->info);
}


int serverdata_update(LocalData * data)
/* Wait until we get new data from the server... */
{
    while (data->old_frame_counter == data->soundinfo->frame_counter) {
        usleep(15000);
    }
    data->old_frame_counter = data->soundinfo->frame_counter;
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
    
    LocalData * s = plugin_register(argv[0], 1);
    /*LocalData * s = serverdata_new("/tmp/x");*/
    gets(stdin);
    serverdata_destroy(s);
    return 0;
}

#endif
