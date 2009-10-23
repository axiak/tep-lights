#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "ipcstructs.h"
#include "server.h"
#include "dmx.h"


int main(int argc, char ** argv)
{
    ServerInfo * info = new_serverenvironment();
    int numc = -1, newc;
    int i;

    while (1) {
        newc = num_clients(info->ipcdata);
        if (newc != numc) {
            printf("Total clients: %d\n", newc);
            numc = newc;
        }
        for (i = 0; i < MAXPLUGINS; i++) {
            /* 193 */
        }
        dmxpanelcltn_sendframe(info->panel);
    }

    destroy_serverenvironment(info);
    return 0;
}

