/* Header file for drawing geometric junk */
#ifndef __GEOM_H
#define __GEOM_H
#include "ipcstructs.h"

RGBPixel BLACK = {0,0,0,1};
RGBPixel RED   = {1,0,0,1};
RGBPixel GREEN = {0,1,0,1};
RGBPixel BLUE  = {0,0,1,1};
RGBPixel YELLOW  = {1,1,0,1};
RGBPixel ORANGE  = {1,.5,0,1};
RGBPixel PURPLE  = {1,0,1,1};

void draw_pixel(ColorLayer *, int x, int y, RGBPixel *);
void draw_line(ColorLayer *,
	       int x0, int y0,
	       int x1, int y1, RGBPixel *);
void draw_gradient(ColorLayer *,
		   int x0, int y0, RGBPixel *,
		   int x1, int y1, RGBPixel *);
void draw_gradient2(ColorLayer *,
		   int x0, int y0, RGBPixel *,
		   int x1, int y1, RGBPixel *);
void draw_blinds(ColorLayer *,
		 int x0, int y0,
		 int x1, int y1, int delta, RGBPixel *);
void draw_circle(ColorLayer *, int x, int y, int radius, RGBPixel *);
void draw_rectangle(ColorLayer *,
		    int x0, int y0,
		    int x1, int y1, RGBPixel *);

#endif
