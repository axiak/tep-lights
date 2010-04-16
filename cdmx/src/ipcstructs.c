#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <sys/sem.h>
#include <signal.h>
#include <errno.h>
#include <math.h>

#include <string.h>

#include "dmx.h"
#include "ipcstructs.h"

#define MIN3(A, B, C) MIN(MIN((A), (B)), (C))
#define MAX3(A, B, C) MAX(MAX((A), (B)), (C))
#define CLAMP(A, LOWER, UPPER) MIN(MAX((A), (LOWER)), (UPPER))


#define ASSERT_SIZES(A,B) \
    if ((A)->width != (B)->width || (A)->height != (B)->height) {   \
        fprintf(stderr, "Size mismatch!\n"); \
        return NULL; \
    }


void rgbpixel_print(RGBPixel * pixel)
{
    if (pixel->red > 0.001 || pixel->green > 0.001 || pixel->blue > 0.001) {
        printf("RGBPixel[%0.4f,%0.4f,%0.4f]\n",
               pixel->red,
               pixel->green,
           pixel->blue);
    }
}

RGBPixel * rgbpixel_create(double red, double green, double blue, double alpha)
{
    RGBPixel * pixel = (RGBPixel *)malloc(sizeof(RGBPixel));
    if (!pixel) return NULL;
    pixel->red = red;
    pixel->green = green;
    pixel->blue = blue;
    pixel->alpha = alpha;
    return pixel;
}

void rgbpixel_destroy(RGBPixel * pixel)
{
    if (pixel) free(pixel);
}

RGBPixel * rgbpixel_copy(RGBPixel * dst, RGBPixel * src)
{
    memcpy(dst, src, sizeof(RGBPixel));
    return dst;
}

RGBPixel * rgbpixel_sethbsvalue(RGBPixel * led, float hue, float brightness, float saturation, float alpha)
{
    int i;
    float f, p, q, t;
    float *r = &led->red;
    float *g = &led->green;
    float *b = &led->blue;

    /* Sanitize inputs */
    brightness = CLAMP(brightness, 0, 1);
    saturation = CLAMP(saturation, 0, 1);
    saturation = 1 - saturation;

    if (!brightness) {
        /* black! */
        *r = *g = *b = 0;
        return led;
    }

    if (!saturation) {
        /* No coloring */
        *r = *g = *b = brightness;
        return led;
    }

    hue *= 6;
    hue = fmod(hue, 6.0);
    if (hue < 0) {
        hue += 6;
    }


    i = floor(hue);
    f = hue - i;
    p = brightness * (1 - saturation);
    q = brightness * (1 - saturation * f);
    t = brightness * (1 - saturation * (1 - f));

    /*printf("f: %0.2f, p: %0.2f, q: %0.2f, t: %0.2f\n",
           f, p, q, t);
    printf("%0.2f, %d\n", hue, i);
    */


    switch (i) {
    case 0:
        *r = brightness;
        *g = t;
        *b = p;
        break;
    case 1:
        *r = q;
        *g = brightness;
        *b = p;
        break;
    case 2:
        *r = p;
        *g = brightness;
        *b = t;
        break;
    case 3:
        *r = p;
        *g = q;
        *b = brightness;
        break;
    case 4:
        *r = t;
        *g = p;
        *b = brightness;
        break;
    default:
        *r = brightness;
        *g = p;
        *b = q;
    }
    led->alpha = alpha;
    return led;
}

void rgbpixel_gethbs(float * dest, RGBPixel * input)
/* An attempt to reverse what's above */
{
    float min, max, delta;
    float *h=&dest[0], *v=&dest[1], *s=&dest[2]; /* shortcut names */

    max = MAX3(input->red, input->green, input->blue);
    min = MIN3(input->red, input->green, input->blue);

    *v = max;
    
    delta = max - min;
    if (!max) {
        *s = 0;
        *h = -1;
        return;
    }
    else {
        *s = 1 - delta / max;
    }

    if (!delta) {
        *h = 0;
    }
    else if (input->red == max) {
        *h = (input->green - input->blue) / delta;
    }
    else if (input->green == max) {
        *h = 2 + (input->blue - input->red) / delta;
    }
    else {
        *h = 4 + (input->red - input->green) / delta;
    }
    *h /= 6.0;
    if (*h < 0) {
        *h += 1;
    }
}


void colorlayer_setall(ColorLayer * layer, float red, float green, float blue, float alpha)
{
    int i;

    if (!red && !green && !blue && !alpha) {
        memset(layer->pixels, 0, sizeof(layer->pixels));
        return;
    }

    for (i = 0; i < layer->width * layer->height; i++) {
        rgbpixel_setvalue(&layer->pixels[i], red, green, blue, alpha);
    }
}


ColorLayer * colorlayer_add(ColorLayer * dst, ColorLayer * src)
{
    ASSERT_SIZES(dst, src)
    int n = dst->width * dst->height;
    int i;
    for (i = 0; i < n; i++) {
        dst->pixels[i].red += src->pixels[i].red;
        dst->pixels[i].green += src->pixels[i].green;
        dst->pixels[i].blue += src->pixels[i].blue;
    }
    return dst;
}

ColorLayer * colorlayer_addalpha(ColorLayer * dst, ColorLayer * src)
{
    ASSERT_SIZES(dst, src)
    int n = dst->width * dst->height;
    float salpha, dalpha;
    int i;
    for (i = 0; i < n; i++) {
        salpha = src->pixels[i].alpha;
        dalpha = dst->pixels[i].alpha;
        dst->pixels[i].red = salpha * src->pixels[i].red + dalpha * dst->pixels[i].red;
        dst->pixels[i].green += salpha * src->pixels[i].green + dst->pixels[i].green * dalpha;
        dst->pixels[i].blue += salpha * src->pixels[i].blue + dalpha * dst->pixels[i].blue;
    }
    return dst;
}

ColorLayer * colorlayer_mult(ColorLayer * dst, ColorLayer * src)
{
    ASSERT_SIZES(dst, src)
    int n = dst->width * dst->height;
    int i;
    for (i = 0; i < n; i++) {
        dst->pixels[i].red *= src->pixels[i].red;
        dst->pixels[i].green *= src->pixels[i].green;
        dst->pixels[i].blue *= src->pixels[i].blue;
    }
    return dst;
}

ColorLayer * colorlayer_colorize(ColorLayer * dst, ColorLayer * alterator)
{
    ASSERT_SIZES(dst, alterator)
    int n = dst->width * dst->height;
    int i;
    float hbs1[3] = {0, 0, 0};
    float hbs2[3] = {0, 0, 0};
    for (i = 0; i < n; i++) {
        rgbpixel_gethbs(hbs2, &alterator->pixels[i]);
        rgbpixel_gethbs(hbs1, &dst->pixels[i]);
        rgbpixel_sethbsvalue(&dst->pixels[i],
                             hbs1[0] + hbs2[0] * 2 - 1,
                             hbs1[1] + hbs2[1] * 2 - 1,
                             hbs1[2],
                             dst->pixels[i].alpha);
    }
    return dst;
}


ColorLayer * colorlayer_copy(ColorLayer * dst, ColorLayer * src) {
    ASSERT_SIZES(dst, src)
    memcpy(dst->pixels, src->pixels, sizeof(src->pixels));
    return dst;
}

ColorLayer * colorlayer_superpose(ColorLayer * top, ColorLayer * bottom)
{
    ASSERT_SIZES(top, bottom)
    int n = top->width * top->height;
    int i;
    RGBPixel * t, * b;
    for (i = 0; i < n; i++) {
        t = &top->pixels[i];
        b = &bottom->pixels[i];
        t->red = t->red * t->alpha + b->red * (1 - t->alpha);
        t->green = t->green * t->alpha + b->green * (1 - t->alpha);
        t->blue = t->blue * t->alpha + b->blue * (1 - t->alpha);
        t->alpha = MIN(1, t->alpha + b->alpha);
    }
    return top;
}

ColorLayer * colorlayer_create()
{
    ColorLayer * layer = (ColorLayer *)malloc(sizeof(ColorLayer));
    if (!layer) {
        fprintf(stderr, "Could not allocate memory for layer");
        exit(2);
    }
    memset(layer, 0, sizeof(ColorLayer));
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

int is_client_running(ClientInfo * info)
{
    if (!info || !info->pid) {
        return 0;
    }

    if (kill(info->pid, 0) < 0) {
        return 0;
    }
    return 1;
}

int num_clients(IPCData * data)
{
    int i;
    int total = 0;
    for (i = 0; i < MAXPLUGINS; i++) {
        if (data->plugins[i].id) {
            if (!is_client_running(&data->plugins[i])) {
                data->plugins[i].id = 0;
            }
            else {
                total ++;
            }
        }
    }
    return total;
}

int begin_lightread(ClientInfo * client)
{
    struct sembuf buffer;
    buffer.sem_num = 0;
    buffer.sem_op = 1;
    semop(client->semid, &buffer, 1);
    return 0;
}

int end_lightread(ClientInfo * client)
{
    struct sembuf buffer;
    buffer.sem_num = 0;
    buffer.sem_op = -1;
    semop(client->semid, &buffer, 1);
    return 0;
}

ColorLayer * plugin_useotherlayer(IPCData * data, int id)
{
    begin_lightread(&data->plugins[id]);
    return &data->plugins[id].layer;
}

void plugin_disuseotherlayer(IPCData * data, int id)
{
    end_lightread(&data->plugins[id]);
}

void colorlayer_pushtocollection(DMXPanelCollection * cltn, ColorLayer * layer)
{
    int r, c;
    RGBPixel * pixel;
    for (r = 0; r < layer->height; r++) {
        for (c = 0; c < layer->width; c++) {
            pixel = colorlayer_getpixel(layer, c, r);
            pixel_setrgb(
                         dmxpanelcltn_getpixel(cltn,
                                               r,
                                               c),
                         pixel->red * pixel->alpha,
                         pixel->green * pixel->alpha,
                         pixel->blue * pixel->alpha
                         );
        }
    }
}

