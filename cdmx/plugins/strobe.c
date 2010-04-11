#include <stdio.h>
#include <cdmx/plugin.h>
#include <math.h>

#define PLUGINID 153

static const int ever = 1;

int main(int argc, char **argv)
{

    LocalData * s = plugin_register(argv[0], PLUGINID);
    ColorLayer * layer = s->layer;
    int on = 0;
    int i;

    for (;ever;) {
	serverdata_update(s);

        if (on) {
            colorlayer_setall(layer, 1, 1, 1, 1);
       }
        else {
            for (i = 0; i < 2; i++) {
                colorlayer_setall(layer, 0, 0, 0, 1);
                serverdata_commitlayer(s);
   	        serverdata_update(s);
            }
        }            
        on = 1 - on;
        serverdata_commitlayer(s);

    }

    serverdata_destroy(s);
    return 0;
}

