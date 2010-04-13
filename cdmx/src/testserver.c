#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "ipcstructs.h"
#include "server.h"
#include "dmx.h"

#ifdef TESTDUMMY
#include "dmxdummy.h"
#endif


int main(int argc, char ** argv)
{
    ServerInfo * info = new_serverenvironment();
    int numc = -1, newc;
    ColorLayer * layer;
    int i;
    int pluginfound = 0;

#ifdef TESTDUMMY
    DMXDummyPanel * panel = dummypanel_create(60, 36);
    info->panel = panel->cltn;
#endif

    ColorLayer * llayer = colorlayer_create();

    for (;;) {
        info->soundinfo->frame_counter++;
        pluginfound = 0;
        newc = num_clients(info->ipcdata);
        if (newc != numc) {
            printf("Total clients: %d\n", newc);
            numc = newc;
        }

        for (i = 0; i < MAXPLUGINS; i++) {
            if (is_client_running(&info->ipcdata->plugins[i])) {
                layer = plugin_useotherlayer(info->ipcdata, i);
                if (pluginfound) {
                    if (!colorlayer_mult(llayer, layer)) {
                        printf("Bad plugin! '%s'\n", info->ipcdata->plugins[i].name);
                        continue;
                    }                        
                }
                else {
                    if (!colorlayer_copy(llayer, layer)) {
                        printf("Bad plugin! '%s'\n", info->ipcdata->plugins[i].name);
                        continue;
                    }
                }
                pluginfound = 1;
                plugin_disuseotherlayer(info->ipcdata, i);
            }
        }


        if (!pluginfound) {
            dmxpanelcltn_wait(info->panel);
            continue;
        }

        colorlayer_pushtocollection(info->panel, llayer);

#ifdef TESTDUMMY
        dummypanel_sendframe(panel);
#else
        dmxpanelcltn_sendframe(info->panel);
#endif

    }

    destroy_serverenvironment(info);
    return 0;
}

