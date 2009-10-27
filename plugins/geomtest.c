#include <stdio.h>
#include <plugin.h>
#include <geom.h>
#include <ipcstructs.h>
#include <dmx.h>

#define PLUGINID 301

int main(int argc, char **argv)
{
    int i, r, c, j;
    LocalData * s = plugin_register(argv[0], PLUGINID);
    ColorLayer * layer = s->layer;
    ColorLayer * layer2;
    RGBPixel color;
    RGBPixel color2;
    double hue;
    i = 0;
    srand(22);
    layer->width = 48;
    layer->height = 24;

    while (1) {
        usleep(100000);
        serverdata_update(s); /* Wait for audio info to update */
        /*colorlayer_setall(layer, 0, 0, 0, 0);*/
        printf("YO\n");
        /* Do stuff to layer... */
        //rgbpixel_sethbsvalue(&color, i/48.0, 1.0, 0.0, 1.0);
        hue = (rand() % 10000) / 10000.0;
        /*rgbpixel_sethbsvalue(&color, hue, 1.0, 1, 1.0);*/
        rgbpixel_setvalue(&color,
                          (rand() % 10000) / 10000.0,
                          (rand() % 10000) / 10000.0,
                          (rand() % 10000) / 10000.0,
                          1);
                          
        rgbpixel_setvalue(&color2, 0, 1.0, 0, 1.0);
        r = i / 48;
        c = i % 48;

        draw_circle(layer, rand()%48, rand()%24, rand()%30, &color);
        /*draw_circle(layer, rand()%48, rand()%24, rand()%30, &color);
          draw_circle(layer, rand()%48, rand()%24, rand()%30, &color);*/
	//draw_line(layer, rand()%96, rand()%48,
	//rand()%96, rand()%48, &color);
	//draw_line(layer, 0, 0,
	//	  rand()%96, rand()%48, &color);
	//draw_blinds(layer, 0, 0, 96, 0, 5, &color);
	//draw_gradient(layer, 0, 0, &color, 48, 0, &color2);
        
        i++;
        i %= 48 * 24;

        /* Commit the layer */
        serverdata_commitlayer(s);
    }

    serverdata_destroy(s);
    return 0;
}

