#ifndef __IPCSTRUCTS_H
#define __IPCSTRUCTS_H

#include "dmx.h"
#include "beat.h"

#define MAINSEMFILE "/etc/resolv.conf"
#define PIXELWIDTH 60
#define PIXELHEIGHT 36
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

#ifdef __cplusplus
extern "C" {
#endif
    /* Used to signal when you are reading. */
    int begin_lightread(ClientInfo * client);
    int end_lightread(ClientInfo * client);

    void colorlayer_setall(ColorLayer * layer, float red, float green, float blue, float alpha);
    void rgbpixel_print(RGBPixel * pixel);
    ColorLayer * colorlayer_add(ColorLayer * dst, ColorLayer * src);
    ColorLayer * colorlayer_mult(ColorLayer * dst, ColorLayer * src);
    ColorLayer * colorlayer_superpose(ColorLayer * top, ColorLayer * bottom);
    ColorLayer * colorlayer_copy(ColorLayer * dst, ColorLayer * src);

    ColorLayer * colorlayer_colorize(ColorLayer * dst, ColorLayer * alterator);

    ColorLayer * colorlayer_create();
    void colorlayer_destroy(ColorLayer * layer);
    void colorlayer_pushtocollection(DMXPanelCollection * cltn, ColorLayer * layer);
    ColorLayer * colorlayer_addalpha(ColorLayer * dst, ColorLayer * src);

    RGBPixel * rgbpixel_create(double red, double green, double blue, double alpha);
    void rgbpixel_destroy(RGBPixel * pixel);

    RGBPixel * rgbpixel_sethbsvalue(RGBPixel * pixel, float h, float b, float s, float alpha);

    void rgbpixel_gethbs(float * dest, RGBPixel * input);

    RGBPixel * rgbpixel_copy(RGBPixel * dst, RGBPixel * src);

    int num_clients(IPCData * data);
    int is_client_running(ClientInfo * info);

    ColorLayer * plugin_useotherlayer(IPCData * data, int id);
    void plugin_disuseotherlayer(IPCData * data, int id);

    static inline RGBPixel * rgbpixel_setvalue(RGBPixel * pixel, float red, float green, float blue, float alpha)
    {
        pixel->red = red;
        pixel->green = green;
        pixel->blue = blue;
        pixel->alpha = alpha;
        return pixel;
    }

    static inline RGBPixel * rgbpixel_setintvalue(RGBPixel * pixel, int red, int green, int blue, int alpha)
    {
        pixel->red = red / 255.0;
        pixel->green = green / 255.0;
        pixel->blue = blue / 255.0;
        pixel->alpha = alpha / 255.0;
        return pixel;
    }

    static inline RGBPixel * colorlayer_getpixel(ColorLayer * layer, int x, int y)
    {
        if (x >= layer->width || y >= layer->height) {
            fprintf(stderr, "Invalid pixel called [%d x %d]: (%d, %d)\n",
                    layer->width, layer->height, x, y);
            return NULL;
        }
        int i = x * layer->height + y;
        return &layer->pixels[i];
    }


#ifdef __cplusplus
}
#endif


#endif
