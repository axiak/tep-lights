#include <stdio.h>
#include <plugin.h>
#include <geom.h>
#include <math.h>
#include <stdlib.h>

#include "sonogram-slow.h"

#define PLUGINID 103

enum {ever = 1,
      SLOWNESS = 3};

void set_color_temperature(RGBPixel * target, float tempurature);


int main(int argc, char **argv)
{
    int r, i, j;
    LocalData * s = plugin_register(argv[0], PLUGINID);
    ColorLayer * layer = s->layer;
    RGBPixel * cur;
    RGBPixel from_fft;
    int slowness = SLOWNESS;
    int vertical_bin = 1;
    int vertical_offset = 0;
    double max_avg, sum_avg;
    int bins;
    CircleBuf * vals, *last;

    switch (argc) {
    case 4:
        vertical_offset = atoi(argv[3]);
    case 3:
        vertical_bin = atoi(argv[2]);
    case 2:
        slowness = atoi(argv[1]);
        break;
    }

    vertical_offset += 2;
    bins = vertical_bin * layer->height;


    last = vals = circlebuf_create(bins,
                                   layer->width * slowness);

    while (last->prev != NULL) {
        last = last->prev;
    }

    for (;ever;) {
        serverdata_update(s); /* Wait for audio info to update */

        max_avg = sum_avg = 0;
        for (r = 0; r < bins; r++) {
            if (s->soundinfo->long_avg[r + vertical_offset] > max_avg)
                max_avg = s->soundinfo->long_avg[r + vertical_offset];
            sum_avg += s->soundinfo->long_avg[r + vertical_offset];
        }
        sum_avg /= bins;

        for (r = 0; r < bins; r++) {
            last->data[r] = pow(s->soundinfo->fft[r + vertical_offset] / sum_avg / 4, 2);
        }
        last->prev = vals;
        vals = last;
        colorlayer_setall(layer, 0, 0, 0, 1);

        for (i = 0; last->prev != vals; i++, last = last->prev) {
            for (r = 0; r < layer->height; ++r) {
                for (j = 0; j < vertical_bin; j++) {
                    set_color_temperature(&from_fft, last->data[vertical_bin * r + j] / (float)slowness / (float)vertical_bin);
                    cur = colorlayer_getpixel(layer, layer->width - i / slowness - 1, r);
                    rgbpixel_setvalue(cur,
                                      cur->red + from_fft.red,
                                      cur->green + from_fft.green,
                                      cur->blue + from_fft.blue,
                                      1);
                }
            }
        }


        /* Commit the layer */
        serverdata_commitlayer(s);
    }

    serverdata_destroy(s);
    return 0;
}



CircleBuf * circlebuf_create(int rows, int cols)
{
    int i;
    CircleBuf * buf, * ptr;
    if (!cols) return NULL;

    buf = (CircleBuf *)malloc(sizeof(CircleBuf));
    buf->data = (double *)calloc(sizeof(double), rows);
    ptr = buf;
    for (i = 1; i < cols - 1; i++) {
        ptr->prev = (CircleBuf *)malloc(sizeof(CircleBuf));
        ptr->data = (double *)calloc(sizeof(double), rows);
        ptr = ptr->prev;
    }
    ptr->data = (double *)calloc(sizeof(double), rows);
    ptr->prev = NULL;
    return buf;
}


void circlebuf_destroy(CircleBuf * c)
{
    CircleBuf * ptr;
    while (c) {
        if (c->data)
            free(c->data);
        ptr = c;
        c = c->prev;
        free(ptr);
    }
    free(c);
}


void set_color_temperature(RGBPixel * target, float tempurature)
{
    float r, g, b;
    r = MIN(MAX( tempurature, 0), 1);
    g = MIN(MAX( tempurature - .5, 0), 1);
    b = MIN(MAX(2 * tempurature, 0), 1);
    rgbpixel_setvalue(target, r, g, b, 1);
}
