#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <sys/sem.h>
#include <signal.h>
#include <errno.h>

#include <string.h>

#include "ipcstructs.h"

RGBPixel * colorlayer_getpixel(ColorLayer * layer, int x, int y)
{
    int i = x * layer->width + y;
    return layer->pixels + i;
}

void colorlayer_setall(ColorLayer * layer, float red, float green, float blue, float alpha)
{
    int i;

    for (i = 0; i < layer->width * layer->height; i++) {
        rgbpixel_setvalue(&layer->pixels[i], red, green, blue, alpha);
    }
}

ColorLayer * colorlayer_add(ColorLayer * dst, ColorLayer * src)
{
    int n = dst->width * dst->height;
    int i;
    for (i = 0; i < n; i++) {
        dst->pixels[i].red += src->pixels[i].red;
        dst->pixels[i].green += src->pixels[i].green;
        dst->pixels[i].blue += src->pixels[i].blue;
    }
    return dst;
}

ColorLayer * colorlayer_mult(ColorLayer * dst, ColorLayer * src)
{
    int n = dst->width * dst->height;
    int i;
    for (i = 0; i < n; i++) {
        dst->pixels[i].red *= dst->pixels[i].red + src->pixels[i].red;
        dst->pixels[i].green *= dst->pixels[i].green + src->pixels[i].green;
        dst->pixels[i].blue *= src->pixels[i].blue;
    }
    return dst;
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
}

int end_lightread(ClientInfo * client)
{
    struct sembuf buffer;
    buffer.sem_num = 0;
    buffer.sem_op = 1;
    semop(client->semid, &buffer, 1);
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

