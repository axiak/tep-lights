#ifndef __IPCSTRUCTS_H
#define __IPCSTRUCTS_H

#include "dmx.h"
#include "beat.h"

#define MAINSEMFILE "/etc/resolv.conf"
#define PIXELWIDTH 48
#define PIXELHEIGHT 24
#define MAXPLUGINS 96


/* Define things that we take for granted when passing information
   back and forth. */


typedef struct {
    float red;
    float green;
    float blue;
    float alpha;
} RGBPixel;

typedef struct {
    RGBPixel pixels[PIXELHEIGHT * PIXELWIDTH];
    int width;
    int height;
} ColorLayer;

typedef struct {
    ColorLayer layer;
    char name[10];
    int id;
    int idx;
    int semid;
    int pid;
    unsigned char input_plugins[MAXPLUGINS];
} ClientInfo;

typedef struct {
    SoundInfo soundinfo;
    ClientInfo plugins[MAXPLUGINS];
} IPCData;

/* Used to signal when you are reading. */
int begin_lightread(ClientInfo * client);
int end_lightread(ClientInfo * client);

RGBPixel * colorlayer_getpixel(ColorLayer * layer, int x, int y);
void colorlayer_setall(ColorLayer * layer, float red, float green, float blue, float alpha);
void rgbpixel_print(RGBPixel * pixel);
ColorLayer * colorlayer_add(ColorLayer * dst, ColorLayer * src);
ColorLayer * colorlayer_mult(ColorLayer * dst, ColorLayer * src);
ColorLayer * colorlayer_superpose(ColorLayer * top, ColorLayer * bottom);
ColorLayer * colorlayer_copy(ColorLayer * dst, ColorLayer * src);

ColorLayer * colorlayer_create();
void colorlayer_destroy(ColorLayer * layer);
void colorlayer_pushtocollection(DMXPanelCollection * cltn, ColorLayer * layer);
ColorLayer * colorlayer_addalpha(ColorLayer * dst, ColorLayer * src);

RGBPixel * rgbpixel_setvalue(RGBPixel * pixel, float red, float green, float blue, float alpha);

RGBPixel * rgbpixel_sethbsvalue(RGBPixel * pixel, float h, float b, float s, float alpha);

int num_clients(IPCData * data);
int is_client_running(ClientInfo * info);

ColorLayer * plugin_useotherlayer(IPCData * data, int id);
void plugin_disuseotherlayer(IPCData * data, int id);



#endif
