#include <stdio.h>
#include <plugin.h>

#define PLUGINID 101

int main(int argc, char **argv)
{
    int i;
    LocalData * s = plugin_register(argv[0], PLUGINID);
    ColorLayer * layer = s->layer;
    ColorLayer * layer2;

    while (1) {
        serverdata_update(s); /* Wait for audio info to update */

        /* Get other plugin information */
        for (i = 0; i < MAXPLUGINS; i++) {
            if (s->info->input_plugins[i]) {
                /* The plugin is one of its inputs, we should use it now. */
                layer2 = plugin_useotherlayer(s, i);
                /* do stuff with layer2...*/
                colorlayer_add(layer, layer2);                
                plugin_disuseotherlayer(s, i);
            }
        }

        /* Doo stuff to layer... */
        


        /* Commit the layer */
        serverdata_commitlayer(s);
    }

    serverdata_destroy(s);
    return 0;
}

