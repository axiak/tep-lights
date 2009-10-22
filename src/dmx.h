#ifndef __DMX_H
#define __DMX_H
#include <sys/socket.h>

#define SZ unsigned int

/* Structures for controlling DMX panels */
typedef struct {
    float red;
    float green;
    float blue;
} RGBLed;

typedef struct {
    RGBLed * led;
    SZ size;
} LEDArray;


/* LED Mapping function */
/* typedef int (*ledmap)(int, int);*/

typedef struct {
    char * ip;
    unsigned short port;
    unsigned char dmxport;
    SZ width;
    SZ height;
    int (*func)(int, int);
    LEDArray * leds;
    int sockfd;
    struct sockaddr * server_addr;
    unsigned char * netbuffer;
} DMXPanel;


/* Initializers */
LEDArray * ledarray_create(SZ size);

/* If mapfunc is null, then the default of (r + 12*(5 - c)) */
DMXPanel * dmxpanel_create(char * ip, unsigned short port, int dmxport, SZ width, SZ height, int (* mapfunc)(int, int));


/* Destroyers */
void ledarray_destroy(LEDArray * ledarray);
void dmxpanel_destroy(DMXPanel * dmxpanel);

/* Other functions */
int dmxpanel_sendframe(DMXPanel * panel);
extern inline RGBLed * dmxpanel_getpixel(DMXPanel * dmxpanel, SZ x, SZ y);

RGBLed * pixel_setrgb(RGBLed * led, float red, float green, float blue);
RGBLed * pixel_sethue(RGBLed * led, float hue, float brightness, float saturation);

/* These operate such that the destination is dst.
   I.e.: dst <- dst * src
*/
RGBLed * pixel_add(RGBLed * dst, RGBLed * src);
RGBLed * pixel_multiply(RGBLed * dst, RGBLed * src);

#ifndef MIN
#define MIN(a, b) (((a) < (b)) ? (a) : (b))
#endif
#ifndef MAX
#define MAX(a, b) (((a) > (b)) ? (a) : (b))
#endif



#endif
