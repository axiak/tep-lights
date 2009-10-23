#include <stdio.h>
#include <plugin.h>

#define PLUGINID 101

int main(int argc, char **argv)
{
    int i, r, c;
    LocalData * s = plugin_register(argv[0], PLUGINID);
    ColorLayer * layer = s->layer;
    ColorLayer * layer2;
    
    while (1) {
        serverdata_update(s); /* Wait for audio info to update */

        /* Get other plugin information */
        for (i = 0; i < MAXPLUGINS; i++) {
            if (s->info->input_plugins[i]) {
                /* The plugin is one of its inputs, we should use it now. */
                layer2 = plugin_useotherlayer(s->ipcdata, i);
                /* do stuff with layer2...*/
                colorlayer_add(layer, layer2);                
                plugin_disuseotherlayer(s->ipcdata, i);
            }
        }

        /* Do stuff to layer... */
        r = i / 48;
        c = i % 48;

        rgbpixel_setvalue(colorlayer_getpixel(layer,
                                              c, r),
                          0, 1, 0, 0);

        i = (i + 1) % (48  * 24);

        /* Commit the layer */
        serverdata_commitlayer(s);
    }

    serverdata_destroy(s);
    return 0;
}

