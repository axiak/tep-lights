#include <stdio.h>
#include <plugin.h>
#include <geom.h>

#define PLUGINID 102

int main(int argc, char **argv)
{
    int i, r, c, j;
    LocalData * s = plugin_register(argv[0], PLUGINID);
    ColorLayer * layer = s->layer;
    ColorLayer * layer2;

    i = 0;
    double avg = 0;
    while (1) {
        serverdata_update(s); /* Wait for audio info to update */

        for (i = 46; i >= 0; i--) {
            for (j = 0; j < 24; j++) {
                draw_pixel(layer, i, j, colorlayer_getpixel(layer, i + 1, j));
            }
        }

        double max = 0;
        for (i = 0; i < 24; i++) {
            if (s->soundinfo->fft[i] > max) {
                max = s->soundinfo->fft[i];
            }
        }

        avg = 0.8 * max + 0.2 * avg;

        for (i = 0; i < 24; i++) {
            rgbpixel_setvalue(colorlayer_getpixel(layer,
                                                  47, i),
                              .5, 0, .4,
                               (s->soundinfo->fft[i] / avg * 0.7)
                              );
        }

        /* Commit the layer */
        serverdata_commitlayer(s);
    }

    serverdata_destroy(s);
    return 0;
}

