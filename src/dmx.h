#ifndef __DMX_H
#define __DMX_H

#define SZ unsigned int

/* Structures for controlling DMX panels */

typedef struct {
  unsigned char red;
  unsigned char green;
  unsigned char blue;
} RGBLed;

typedef struct {
  RGBLed * led;
  SZ size;
} LEDArray;

typedef struct {
  char * ip;
  SZ width;
  SZ height;
  int sockfd;
  LEDArray * leds;
} DMXPanel;

/* Initializers */
LEDArray * ledarray_create(SZ size);
DMXPanel * dmxpanel_create(char * ip, SZ width, SZ height);


/* Destroyers */
void ledarray_destroy(LEDArray * ledarray);
void dmxpanel_destroy(DMXPanel * dmxpanel);

/* Other functions */
extern inline RGBLed * dmxpanel_getpixel(DMXPanel * dmxpanel, SZ x, SZ y);

void pixel_setrgb(unsigned char red, unsigned char green, unsigned char blue);
void pixel_sethsv(un


#endif
