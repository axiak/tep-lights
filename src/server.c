#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <sys/sem.h>

#include <sys/time.h>
#include <time.h>

#include "ipcstructs.h"
#include "server.h"

/*
typedef struct {
    IPCData * ipcdata;
    SoundInfo * soundinfo;
    DMXPanelCollection * panel;
    int shmid;
    int semid;
} ServerInfo;
*/

ServerInfo * new_serverenvironment()
{
    key_t key;
    int i, j;
    ServerInfo * info = (ServerInfo *)malloc(sizeof(ServerInfo));

    /* Create shared memory stuff */
    key = ftok(MAINSEMFILE, 'a');
    /* Remove old shm memory segment */
    {
        struct shmid_ds output;
        int shmid = shmget(key, 0, 0666);

        if (shmid >= 0) {
            shmctl(shmid, IPC_RMID, &output);
        }
    }

    if ((info->shmid = shmget(key, sizeof(IPCData), IPC_CREAT | 0666)) < 0) {
        fprintf(stderr, "Could not create shared memory");
        free(info);
        return NULL;
    }
    info->ipcdata = (IPCData *)shmat(info->shmid, NULL, 0);
    info->soundinfo = &info->ipcdata->soundinfo;
    memset(info->ipcdata, 0, sizeof(IPCData));

    printf("Created key %d\n", key);
    for (i = 0; i < MAXPLUGINS; i++) {
        info->ipcdata->plugins[i].layer.width = 48;
        info->ipcdata->plugins[i].layer.height = 24;
    }

    /* Create semaphores */
    key = ftok(MAINSEMFILE, 'L');
    info->semid = semget(key, MAXPLUGINS, 0666 | IPC_CREAT);
    return info;
}

void destroy_serverenvironment(ServerInfo * info)
{
    /* Remove our shared memory segment. */
    struct shmid_ds output;

    semctl(info->semid, 0, IPC_RMID, 0);

    shmctl(info->shmid, IPC_RMID, &output);
    shmdt(info->ipcdata);
    info->ipcdata = info->soundinfo = 0;
    free(info);
    return;
}

#ifdef SERVERTEST
int main(int argc, char ** argv) {
    ServerInfo * info = new_serverenvironment();
    int numc = -1, newc;
    
    while (1) {
        newc = num_clients(info->ipcdata);
        if (newc != numc) {
            printf("Total clients: %d\n", newc);
            numc = newc;
        }
        usleep(100000);
    }

    destroy_serverenvironment(info);
    return 0;
}
#endif
