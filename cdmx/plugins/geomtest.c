#include <stdio.h>
#include <stdlib.h>
#include <plugin.h>
#include <geom.h>
#include <ipcstructs.h>
#include <dmx.h>

#define PLUGINID 301

enum {ever=1};

int main(int argc, char **argv)
{
    int i, r, c;
    LocalData * s = plugin_register(argv[0], PLUGINID);
    ColorLayer * layer = s->layer;
    RGBPixel color;
    RGBPixel color2;
    double hue;
    i = 0;
    srand(22);
    for (;ever;) {
        usleep(100000);
        serverdata_update(s); /* Wait for audio info to update */
        hue = (rand() % 10000) / 10000.0;
        rgbpixel_setvalue(&color,
                          (rand() % 10000) / 10000.0,
                          (rand() % 10000) / 10000.0,
                          (rand() % 10000) / 10000.0,
                          1);
                          
        rgbpixel_setvalue(&color2, 0, 1.0, 0, 1.0);
        r = i / layer->width;
        c = i % layer->width;

        draw_circle(layer, rand()%layer->width, rand()%layer->height, rand()%30, &color);
        i++;
        i %= layer->width * layer->height;

        /* Commit the layer */
        serverdata_commitlayer(s);
    }

    serverdata_destroy(s);
    return 0;
}

