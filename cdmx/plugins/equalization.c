#include <stdio.h>
#include <cdmx/plugin.h>
#include <math.h>

#define PLUGINID 198


int main(int argc, char **argv)
{
    int r, c;
    LocalData * s = plugin_register(argv[0], PLUGINID);
    ColorLayer * layer = s->layer;
    int on = 0;
    int i;
    double max_avg, sum_avg;
    int bins = layer->width / 2;
    double val;

    for (;;) {
        serverdata_update(s);

        colorlayer_setall(layer, 0, 0, 0, 1);

        max_avg = sum_avg = 0;
        for (c = 2; c < bins + 2; c++) {
            if (s->soundinfo->long_avg[c] > max_avg)
                max_avg = s->soundinfo->long_avg[c];
            sum_avg += s->soundinfo->long_avg[c];
        }
        sum_avg /= bins;

        for (c = 0; c < bins; c++) {
            val = pow(s->soundinfo->fft[c + 2] / sum_avg / 8, 2);
            if (val < 0.01)
                continue;
            for (r = 0; r < MIN(val * layer->height, layer->height); r++) {
                rgbpixel_setvalue(
                                  colorlayer_getpixel(layer,
                                                      2 * c, r),
                                  0, 0.5, 0.5, 1);
                rgbpixel_setvalue(
                                  colorlayer_getpixel(layer,
                                                      2 * c + 1, r),
                                  0, 0.5, 0.5, 1);
            }
        }

        serverdata_commitlayer(s);

    }

    serverdata_destroy(s);
    return 0;
}

