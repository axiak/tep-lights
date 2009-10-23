#ifndef __IPCSTRUCTS_H
#define __IPCSTRUCTS_H


#define MAINSEMFILE __FILE__
#define PIXELWIDTH 48
#define PIXELHEIGHT 24
#define MAXPLUGINS 96
/* Define things that we take for granted when passing information
   back and forth. */

typedef struct {
    float fft[256];
    float volumehistory[24];
    unsigned char bpm_valid;
    unsigned char bpm;
    float bpm_certainty;
    unsigned long frame_counter;
} SoundInfo;

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
    int semid;
} ClientInfo;

typedef struct {
    SoundInfo soundinfo;
    ClientInfo plugins[MAXPLUGINS];
} IPCData;

RGBPixel * colorlayer_getpixel(ColorLayer * layer, int x, int y);
void colorlayer_setall(ColorLayer * layer, float red, float green, float blue, float alpha);
ColorLayer * colorlayer_create();
void colorlayer_destroy(ColorLayer * layer);

static inline RGBPixel * rgbpixel_setvalue(RGBPixel * pixel, float red, float green, float blue, float alpha)
{
    pixel->red = red;
    pixel->green = green;
    pixel->blue = blue;
    pixel->alpha = alpha;
    return pixel;
}



#endif
