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
    ServerInfo * info = (ServerInfo *)malloc(sizeof(ServerInfo));

    key = ftok(MAINSEMFILE, 0);
    if ((info->shmid = shmget(key, sizeof(IPCData), IPC_CREAT | 0666)) < 0) {
        fprintf(stderr, "Could not create shared memory");
        free(info);
        return NULL;
    }
    printf("Key: %d\n", key);
    info->ipcdata = (IPCData *)shmat(info->shmid, NULL, 0);
    memset(info->ipcdata, 0, sizeof(IPCData));

    return info;
}

void destroy_serverenvironment()
{
    return;


}

#ifdef SERVERTEST
int main(int argc, char ** argv) {
    ServerInfo * info = new_serverenvironment();
    int c = getc(stdin);
    return 0;
}
#endif
