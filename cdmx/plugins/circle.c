#include <stdio.h>
#include <plugin.h>
#include <geom.h>
#include <ipcstructs.h>
#include <dmx.h>

#define PLUGINID 303

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
    float avg_vol = 0;
    while (1) {
        serverdata_update(s); /* Wait for audio info to update */
        
        /* Do stuff to layer... */
	//        rgbpixel_sethbsvalue(&color, i/48.0, 1.0, 0.0, 1.0);
	//        rgbpixel_setvalue(&color2, 0, 1.0, 0, 1.0);

	colorlayer_setall(layer, 0, 0, 0, 0);
	
	avg_vol = (30*avg_vol + s->soundinfo->volumehistory[0])/31.0;
	float dvol = (s->soundinfo->volumehistory[0]-avg_vol)/avg_vol;

        draw_circle(layer, 24, 12, dvol+10, &RED);
        draw_circle(layer, 24, 12, rand()%10, &RED);
	//draw_line(layer, rand()%96, rand()%48,
	//rand()%96, rand()%48, &color);
	//draw_line(layer, 0, 0,
	//	  rand()%96, rand()%48, &color);
	//draw_blinds(layer, 0, 0, 96, 0, 5, &color);
	//draw_gradient(layer, 0, 0, &color, 48, 0, &color2);
        
        /* Commit the layer */
        serverdata_commitlayer(s);
    }

    serverdata_destroy(s);
    return 0;
}

