#include <stdlib.h>

#include "ipstructs.h"

RGBPixel * colorlayer_getpixel(ColorLayer * layer, int x, int y)
{
    int i = x * layer->width + y;
    return layer->pixels + i;
}

static inline RGBPixel * rgbpixel_setvalue(RGBPixel * pixel, float red, float green, float blue, float alpha)
{
    pixel->red = red;
    pixel->green = green;
    pixel->blue = blue;
    pixel->alpha = alpha;
}

void colorlayer_setall(ColorLayer * layer, float red, float green, float blue, float alpha)
{
    int i;

    for (i = 0; i < layer->width * layer->height; i++) {
        rgbpixel_setvalue(layer->pixels[i], red, green, blue, alpha);
    }
}

ColorLayer * colorlayer_create()
{
    ColorLayer * layer = (ColorLayer *)malloc(sizeof(ColorLayer));
    if (!layer) {
        fprintf(stderr, "Could not allocate memory for layer");
        exit(2);
    }
    layer->width = PIXELWIDTH;
    layer->height = PIXELHEIGHT;
    return layer;
}


void colorlayer_destroy(ColorLayer * layer)
{
    if (layer) {
        free(layer);
    }
}

#endif
