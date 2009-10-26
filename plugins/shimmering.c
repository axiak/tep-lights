#include <stdio.h>
#include <plugin.h>
#include <math.h>

#define PLUGINID 105

int main(int argc, char **argv)
{
    int i, r, c, j;
    double x, y;
    LocalData * s = plugin_register(argv[0], PLUGINID);
    ColorLayer * layer = s->layer;

    double width = 1.0, hue = 0, shimmer_angle = 0,
        center_x = 0, center_y = 0, dx = 0.001, dy = 0.001, dist;

    for (;;) {
        serverdata_update(s);
        hue += 2 / 255.0;
        shimmer_angle += 0.05;
        center_x += dx * cos(shimmer_angle / 100);
        center_y += dy * sin(shimmer_angle / 100);

        if (center_x > width) {
            dx = -dx;
            center_x = 1;
        }
        else if (center_x < -1) {
            dx = -dx;
            center_x = -1;
        }

        if (center_y > 1) {
            dy = -dy;
            center_y = 1;
        }
        else if (center_y < -1) {
            dy = -dy;
            center_y = -1;
        }

        for (r = 0; r < layer->height; r++) {
            for (c = 0; c < layer->width; c++) {
                x = c / (double)layer->width - 0.5;
                y = r / (double)layer->height - 0.5;
                dist = cos(shimmer_angle / 10.0) * x * y + cos(shimmer_angle) * x * x + sin(shimmer_angle) * y * y;
                rgbpixel_sethbsvalue(
                                     colorlayer_getpixel(layer, c, r),
                                     hue + dist / 2.5, 1, 0, 1);
            }
        }
        
        /* Commit the layer */
        serverdata_commitlayer(s);
    }

    serverdata_destroy(s);
    return 0;
}

