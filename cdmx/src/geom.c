#include <stdlib.h>
#include <string.h>
#include "geom.h"
#include "ipcstructs.h"

RGBPixel BLACK = {0,0,0,1};
RGBPixel RED   = {1,0,0,1};
RGBPixel GREEN = {0,1,0,1};
RGBPixel BLUE  = {0,0,1,1};
RGBPixel YELLOW  = {1,1,0,1};
RGBPixel ORANGE  = {1,.5,0,1};
RGBPixel PURPLE  = {1,0,1,1};

void draw_pixel(ColorLayer * cl, int x, int y, RGBPixel * color) {
  if(0 <= x && x < cl->width &&
     0 <= y && y < cl->height) {
    memcpy(colorlayer_getpixel(cl, x, y), color, sizeof(RGBPixel));
  }
}

void draw_line(ColorLayer * cl,
	       int x0, int y0, int x1, int y1, RGBPixel * color) {
  char steep = abs(y1-y0) > abs(x1-x0);
  if(steep) {
    int s = x0;
    x0 = y0; y0 = s;
    s = x1;
    x1 = y1; y1 = s;
  }
  if(x0 > x1) {
    int s = x0;
    x0 = x1; x1 = s;
    s = y0;
    y1 = y0; y0 = s;
  }
  int dx = x1 - x0;
  int dy = abs(y1 - y0);
  int error = dx / 2;
  int ystep;
  int y = y0;
  if(y0 < y1)
    ystep = 1;
  else
    ystep = -1;
  for(int x = x0; x <= x1; x++) {
    if(steep)
      draw_pixel(cl,y,x,color);
    else
      draw_pixel(cl,x,y,color);
    error = error - dy;
    if(error < 0) {
      y += ystep;
      error += dx;
    }
  }
}

void draw_gradient(ColorLayer * cl,
		   int x0, int y0, RGBPixel * color1,
		   int x1, int y1, RGBPixel * color2) {
  RGBPixel combo;
  float bottom = (y1-y0)*(y1-y0)+(x1-x0)*(x1-x0);
  for(int x = 0; x < cl->width; x++) {
    for(int y = 0; y < cl->height; y++) {
      float a = ((x1-x0)*(x-x0) + (y1-y0)*(y-y0))/bottom;
      if(a <= 0) {
	draw_pixel(cl, x, y, color1);
      } else if(a >= 1) {
	draw_pixel(cl, x, y, color2);
      } else {
	combo.red = (1-a)*color1->red + a*color2->red;
	combo.green = (1-a)*color1->green + a*color2->green;
	combo.blue = (1-a)*color1->blue + a*color2->blue;
	combo.alpha = (1-a)*color1->alpha + a*color2->alpha;
	draw_pixel(cl, x, y, &combo);
      }
    }
  }
}
void draw_gradient2(ColorLayer * cl,
		   int x0, int y0, RGBPixel * color1,
		   int x1, int y1, RGBPixel * color2) {
  RGBPixel combo;
  float bottom = (y1-y0)*(y1-y0)+(x1-x0)*(x1-x0);
  for(int x = 0; x < cl->width; x++) {
    for(int y = 0; y < cl->height; y++) {
      float a = ((x1-x0)*(x-x0) + (y1-y0)*(y-y0))/bottom;
      if( a >= 0 && a <= 1) {
	combo.red = (1-a)*color1->red + a*color2->red;
	combo.green = (1-a)*color1->green + a*color2->green;
	combo.blue = (1-a)*color1->blue + a*color2->blue;
	combo.alpha = (1-a)*color1->alpha + a*color2->alpha;
	draw_pixel(cl, x, y, &combo);
      }
    }
  }
}

void draw_blinds(ColorLayer * cl,
		 int x0, int y0,
		 int x1, int y1, int delta, RGBPixel * color) {
  if(x1 < x0) {
    int s = x0;
    x0 = x1; x1 = s;
  }
  if(y1 < y0) {
    int s = y0;
    y0 = y1; y1 = s;
  }
  int dx = x1 - x0;
  int dy = y1 - y0;
  for(float x = x0; x <= x1; x += (float)dx/delta) {
    for(float y = y0; y <= y1; y += (float)dy/delta) {
      draw_line(cl,
		x - dy*cl->width, y + dx*cl->width,
		x + dy*cl->width, y - dx*cl->width,
		color);
    }
  }
}

void draw_circle(ColorLayer * cl,
		 int cx, int cy, int radius, RGBPixel * col) {
  int error = -radius;
  int x = radius;
  int y = 0;
  while(x >= y) {
    draw_pixel(cl, cx + x, cy + y, col);
    if(x != 0) draw_pixel(cl, cx - x, cy + y, col);
    if(y != 0) draw_pixel(cl, cx + x, cy - y, col);
    if(x != 0 && y != 0) draw_pixel(cl, cx - x, cy - y, col);
    if(x != y) {
      draw_pixel(cl, cx + y, cy + x, col);
      if(y != 0) draw_pixel(cl, cx - y, cy + x, col);
      if(x != 0) draw_pixel(cl, cx + y, cy - x, col);
      if(y != 0 && x != 0) draw_pixel(cl, cx - y, cy - x, col);
    }

    error += y;
    ++y;
    error += y;
    if(error >= 0) {
      --x;
      error -= x;
      error -= x;
    }
  }
}

void draw_rectangle(ColorLayer * cl,
		    int x0, int y0,
		    int x1, int y1, RGBPixel * color) {
  if(x0 > x1) {
    int s = x0;
    x0 = x1; x1 = s;
  }
  if(y0 > y1) {
    int s = y0;
    y0 = y1; y1 = s;
  }
  for(int x = x0; x <= x1; x++) {
    for(int y = y0; y <= y1; y++) {
      draw_pixel(cl, x, y, color);
    }
  }
}
