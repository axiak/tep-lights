#ifndef __DMXDUMMY_H
#define __DMXDUMMY_H

#include <SDL/SDL.h>
#include "dmx.h"


typedef struct {
    DMXPanel * panel;
    DMXPanelCollection * cltn;
    SDL_Surface *screen;
    int width;
    int height;
} DMXDummyPanel;

DMXDummyPanel * dummypanel_create(int width, int height);
void dummypanel_sendframe(DMXDummyPanel * panel);
void dummypanel_destroy(DMXDummyPanel * panel);

#endif
