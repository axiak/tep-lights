#include <stdlib.h>
#include <SDL/SDL.h>
#include <sys/signal.h>

#include "dmx.h"
#include "dmxdummy.h"

#ifndef FLOAT2CHAR
#define FLOAT2CHAR(A) ((unsigned char)(256 * (MIN(MAX(A, 0), 0.999))))
#endif

#define BINSIZE 15

float _getalpha(int i, int j, int width);

/* TODO: FIX THIS! */

DMXDummyPanel * dummypanel_create(int width, int height)
{
    DMXDummyPanel * panel = (DMXDummyPanel *)malloc(sizeof(DMXDummyPanel));
    DMXPanel * dpanel = dmxpanel_create(0, 0, 0, width, height, 0);
    DMXPanelCollection * cltn = dmxpanelcltn_create(1, 1);
    SDL_Surface *screen;
    dmxpanelcltn_setpanel(cltn, dpanel, 0, 0);

    panel->panel = dpanel;
    panel->cltn = cltn;

    if ( SDL_Init(SDL_INIT_VIDEO | SDL_INIT_NOPARACHUTE) < 0 ) {
        fprintf(stderr, "Unable to init SDL: %s\n", SDL_GetError());
        exit(1);
    }
    signal(SIGINT, SIG_DFL);

    panel->width = width;
    panel->height = height;

    screen = SDL_SetVideoMode(width * BINSIZE, height * BINSIZE, 16, SDL_HWSURFACE );
    panel->screen = screen;
    if ( screen == NULL ) {
        fprintf(stderr, "Unable to set 640x480 video: %s\n", SDL_GetError());
        exit(1);
    }
    SDL_WM_SetCaption("tEp DMX Screen", "DMX");
    return panel;
    
}

void dummypanel_destroy(DMXDummyPanel * panel)
{
    atexit(SDL_Quit);
    free(panel->screen);
    dmxpanelcltn_destroy(panel->cltn);
    free(panel);
}

void dummypanel_sendframe(DMXDummyPanel * panel)
{
    RGBLed * pixel;
    DMXPanel * p = panel->panel;
    SDL_Surface *screen = panel->screen;
    int r, c;
    Uint32 color;
    Uint16 *buf;
    int i, j;
    float alpha;

    if (SDL_MUSTLOCK(screen)) {
        if (SDL_LockSurface(screen) < 0) {
            return;
        }
    }

    for (r = 0; r < p->height; r++) {
        for (c = 0; c < p->width; c++) {
            pixel = dmxpanel_getpixel(p, r, c);
            for (i = 0; i < BINSIZE; i++) {
                for (j = 0; j < BINSIZE; j++) {
                    alpha = _getalpha(i, j, BINSIZE);
                    color = SDL_MapRGB(screen->format,
                                       FLOAT2CHAR(pixel->red * alpha),
                                       FLOAT2CHAR(pixel->green * alpha),
                                       FLOAT2CHAR(pixel->blue * alpha));
                    buf = (Uint16*)screen->pixels + (BINSIZE * r + i) * screen->pitch/2 + (BINSIZE * c + j);
                    *buf = color;
                }
            }

        }
    }

    if (SDL_MUSTLOCK(screen)) {
        SDL_UnlockSurface(screen);
    }
    dmxpanel_wait(p);
    SDL_UpdateRect(screen, 0, 0, 0, 0);
}


#ifdef DMXDUMMY
int main(int argc, char ** argv)
{
    int r, c;
    DMXDummyPanel * panel = dummypanel_create(48, 24);
    DMXPanel * p = panel->panel;
    for (r = 0; r < p->height; r ++) {
        for (c = 0; c < p->width; c++) {
            pixel_setrgb(dmxpanel_getpixel(p, r, c), 1, 0, 0);
        }
    }
    dummypanel_sendframe(panel);
    sleep(1);
    dummypanel_destroy(panel);
    return 0;
}
#endif


float _getalpha(int i, int j, int width)
{
    double distance_squared;
    double center = width / 2.0;

    distance_squared =
        (i - center) * (i - center) +
        (j - center) * (j - center);

    if (distance_squared < 2) {
        return 1;
    }

    if (distance_squared > ((center) * (center))) {
        return 0;
    }

    return 1 - distance_squared / (center * center);
}
