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
    i = 0;
    layer->width = 48;
    layer->height = 24;
    while (1) {
        serverdata_update(s); /* Wait for audio info to update */
        printf("YO\n");
        /* Get other plugin information */

       /*  for (j = 0; j < MAXPLUGINS; j++) { */
/*             if (s->info->input_plugins[j]) { */
/*                 /\* The plugin is one of its inputs, we should use it now. *\/ */
/*                 layer2 = plugin_useotherlayer(s->ipcdata, j); */
/*                 /\* do stuff with layer2...*\/ */
/*                 colorlayer_add(layer, layer2); */
/*                 plugin_disuseotherlayer(s->ipcdata, j); */
/*             } */
/* 	} */


        
        /* Do stuff to layer... */
        rgbpixel_sethbsvalue(&color, i/48.0, 1.0, 0.0, 1.0);
        rgbpixel_setvalue(&color2, 0, 1.0, 0, 1.0);

	//colorlayer_setall(layer, 0, 0, 0, 0);
	
        r = i / 48;
        c = i % 48;

        //draw_circle(layer, rand()%96, rand()%48, rand()%30, &color);
	//draw_line(layer, rand()%96, rand()%48,
	//rand()%96, rand()%48, &color);
	draw_line(layer, 0, 0,
		  rand()%96, rand()%48, &color);
        
        i++;
        i %= 48 * 24;

        /* Commit the layer */
        serverdata_commitlayer(s);
    }

    serverdata_destroy(s);
    return 0;
}

