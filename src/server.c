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

#include "ipcstructs.h"
#include "server.h"
#include "dmx.h"

#define SHMSIZE MAX(10000000, sizeof(IPCData))
/*#define SHMSIZE sizeof(IPCData)*/

ServerInfo * new_serverenvironment()
{
    key_t key;
    int i;
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
        printf("%d\n", errno);
    }

    if ((info->shmid = shmget(key, SHMSIZE, IPC_CREAT | 0666)) < 0) {
        
        fprintf(stderr, "Could not create shared memory: %d [%d] %d", info->shmid,
                sizeof(IPCData), errno);
        free(info);
        return NULL;
    }
    info->ipcdata = (IPCData *)shmat(info->shmid, NULL, 0);
    info->soundinfo = &info->ipcdata->soundinfo;
    memset(info->ipcdata, 0, sizeof(IPCData));

    printf("Created key %d (%d)\n", key, sizeof(IPCData));

    for (i = 0; i < MAXPLUGINS; i++) {
        info->ipcdata->plugins[i].layer.width = 48;
        info->ipcdata->plugins[i].layer.height = 24;
    }

    /* Create semaphores */
    key = ftok(MAINSEMFILE, 'L');
    info->semid = semget(key, MAXPLUGINS, 0666 | IPC_CREAT);


    /* Initialize the panel */
    info->panel = create_default_panels();

    return info;
}

void destroy_serverenvironment(ServerInfo * info)
{
    /* Remove our shared memory segment. */
    struct shmid_ds output;

    semctl(info->semid, 0, IPC_RMID, 0);

    shmctl(info->shmid, IPC_RMID, &output);
    shmdt(info->ipcdata);
    free(info);
    return;
}

