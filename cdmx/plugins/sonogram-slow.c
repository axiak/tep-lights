#include <stdio.h>
#include <plugin.h>
#include <geom.h>
#include <math.h>
#include <stdlib.h>

#include "sonogram-slow.h"

#define PLUGINID 103

#define SLOWNESS 3

enum {ever = 1};

void set_color_temperature(RGBPixel * target, float tempurature);


int main(int argc, char **argv)
{
    int r;
    LocalData * s = plugin_register(argv[0], PLUGINID);
    ColorLayer * layer = s->layer;
    RGBPixel * cur;
    RGBPixel from_fft;
    int i;
    int slowness = SLOWNESS;
    int COLOR = 0;
    double *denoms = (double *)calloc(sizeof(double), s->layer->height);
    double *smoothers = (double *)calloc(sizeof(double), s->layer->height);
    double cur_max, denom=0;

    CircleBuf * vals, *last;

    switch (argc) {
    case 3:
        COLOR = atoi(argv[2]);
    case 2:
        slowness = atoi(argv[1]);
        break;
    }
    last = vals = circlebuf_create(layer->height,
                                   layer->width * slowness);

    while (last->prev != NULL) {
        last = last->prev;
    }

    for (;ever;) {
        serverdata_update(s); /* Wait for audio info to update */

        /* Overall loudness factors */
        for (r = 0; r < layer->height; r++) {
            denoms[r] = 1;
            smoothers[r] = 0;
            if (s->soundinfo->fft[r] > cur_max) {
                cur_max = s->soundinfo->fft[r];
            }
        }
        denom = 0.8 * denom + 0.2 * cur_max;


        for (r = 0; r < layer->height; r++) {
            double val = pow(s->soundinfo->fft[r] / denoms[r] / pow(denom, 0.4), 0.7);
            denoms[r] = denoms[r] * 0.9 + val * 0.1;

            smoothers[r] = val * 0.5 + 0.5 * smoothers[r];
            last->data[r] = smoothers[r];
            /*printf("   %0.2f %0.2f %0.2f\n ", val, smoothers[r], denoms[r]);*/
        }
        last->prev = vals;
        vals = last;
        colorlayer_setall(layer, 0, 0, 0, 1);

        for (i = 0; last->prev != vals; i++, last = last->prev) {
            for (r = 0; r < layer->height; r++) {
                set_color_temperature(&from_fft, last->data[r] / (float)slowness);
                cur = colorlayer_getpixel(layer, layer->width - i / slowness - 1, r);
                rgbpixel_setvalue(cur,
                                  cur->red + from_fft.red,
                                  cur->green + from_fft.green,
                                  cur->blue + from_fft.blue,
                                  1);
                /*
                if (i > slowness) {
                    cur = colorlayer_getpixel(layer, layer->width - i / slowness, r);
                    rgbpixel_setvalue(cur,
                                      cur->red + 0.25 * from_fft.red,
                                      cur->green + 0.25 * from_fft.green,
                                      cur->blue + 0.25 * from_fft.blue,
                                      1);
                }
                if (i < (layer->height - slowness)) {
                    cur = colorlayer_getpixel(layer, layer->width - i / slowness - 2, r);
                    rgbpixel_setvalue(cur,
                                      cur->red + 0.25 * from_fft.red,
                                      cur->green + 0.25 * from_fft.green,
                                      cur->blue + 0.25 * from_fft.blue,
                                      1);
                                      }*/
           
            }
        }


        /* Commit the layer */
        serverdata_commitlayer(s);
    }

    serverdata_destroy(s);
    return 0;
}


/*
typedef struct CircleBuf_s {
    struct CircleBuf_s * pref;
    double * data;
} CircleBuf;
*/

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
