#include <stdio.h>
#include <plugin.h>

#define PLUGINID 101

int main(int argc, char **argv)
{
    int i, r, c, j;
    LocalData * s = plugin_register(argv[0], PLUGINID);
    ColorLayer * layer = s->layer;
    ColorLayer * layer2;
    i = 0;
    layer->width = 48;
    layer->height = 24;
    while (1) {
        serverdata_update(s); /* Wait for audio info to update */

        /* Get other plugin information */

        for (j = 0; j < MAXPLUGINS; j++) {
            if (s->info->input_plugins[j]) {
                /* The plugin is one of its inputs, we should use it now. */
                layer2 = plugin_useotherlayer(s->ipcdata, j);
                /* do stuff with layer2...*/
                colorlayer_add(layer, layer2);
                plugin_disuseotherlayer(s->ipcdata, j);
            }
            }


        /* Do stuff to layer... */
        r = i / 48;
        c = i % 48;

        printf("%d,%d\n", c, r);
        rgbpixel_setvalue(colorlayer_getpixel(layer,
                                              c, r),
                          1, 0, 0, 0);
        


        i++;
        i %= 48 * 24;

        /* Commit the layer */
        serverdata_commitlayer(s);
    }

    serverdata_destroy(s);
    return 0;
}

