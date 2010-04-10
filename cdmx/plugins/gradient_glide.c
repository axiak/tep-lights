#include <stdio.h>
#include <plugin.h>
#include <geom.h>
#include <ipcstructs.h>
#include <dmx.h>
#include <math.h>

#define PLUGINID 301

int main(int argc, char **argv)
{
    int i, r, c, j;
    LocalData * s = plugin_register(argv[0], PLUGINID);
    ColorLayer * layer = s->layer;
    ColorLayer * layer2;
    RGBPixel color;
    RGBPixel color2;
    i = 0;
    layer->width = 48;
    layer->height = 24;
    while (1) {
        serverdata_update(s); /* Wait for audio info to update */
        
        /* Do stuff to layer... */
        rgbpixel_sethbsvalue(&color, i/200.0, 1.0, 0.0, 1.0);
        rgbpixel_sethbsvalue(&color2, i/230.0+0.3, 1.0, 0, 1.0);

	//colorlayer_setall(layer, 0, 0, 0, 0);
	
        //draw_circle(layer, rand()%96, rand()%48, rand()%30, &color);
	//draw_line(layer, rand()%96, rand()%48,
	//rand()%96, rand()%48, &color);
	//draw_line(layer, 0, 0,
	//	  rand()%96, rand()%48, &color);
	//draw_blinds(layer, 0, 0, 96, 0, 5, &color);
	draw_gradient(layer, 0, sin(i/300.0)*24, &color, 48, cos(i/270.0)*24, &color2);
        
        i++;

        /* Commit the layer */
        serverdata_commitlayer(s);
    }

    serverdata_destroy(s);
    return 0;
}

