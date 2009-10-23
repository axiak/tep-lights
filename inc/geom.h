/* Header file for drawing geometric junk */
#ifndef __GEOM_H
#define __GEOM_H
#include "ipcstructs.h"

void draw_pixel(ColorLayer *, int x, int y, RGBPixel *);
void draw_line(ColorLayer *,
	       int x0, int y0,
	       int x1, int y1, RGBPixel *);
void draw_gradient(ColorLayer *,
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
