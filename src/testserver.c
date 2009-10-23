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
    ColorLayer * layer;
    int i;
    int x, y;
    while (1) {
        newc = num_clients(info->ipcdata);
        if (newc != numc) {
            printf("Total clients: %d\n", newc);
            numc = newc;
        }
        for (i = 0; i < MAXPLUGINS; i++) {
            if (is_client_running(&info->ipcdata->plugins[i])) {
                break;
            }
        }

        layer = plugin_useotherlayer(&info->ipcdata, i);
        colorlayer_pushtocollection(info->panel, layer);
        plugin_disuseotherlayer(&info->ipcdata, i);

        dmxpanelcltn_sendframe(info->panel);
    }

    destroy_serverenvironment(info);
    return 0;
}

