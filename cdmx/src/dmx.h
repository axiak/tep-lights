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


typedef struct {
    char * ip;
    unsigned short port;
    unsigned char dmxport;
    SZ width;
    SZ height;
    int (*func)(int, int, int, int);
    LEDArray * leds;
    int sockfd;
    struct sockaddr * server_addr;
    unsigned char * netbuffer;
    double lastupdate;
    int direction;
    int stale;
} DMXPanel;

typedef struct {
    DMXPanel ** panels;
    int width;
    int height;
    int _ledwidth;
    int _ledheight;
} DMXPanelCollection;

#ifdef __cplusplus
extern "C" {
#endif
    /* Initializers */
    LEDArray * ledarray_create(SZ size);

    /* If mapfunc is null, then the default of (r + 12*(5 - c)) */
    DMXPanel * dmxpanel_create(char * ip, unsigned short port, int dmxport, SZ width, SZ height, int (* mapfunc)(int, int, int, int));
    DMXPanel * dmxpanel_createhalfpanel(char * ip, unsigned short port, int dmxport, int direction);
    DMXPanel * dmxpanel_createfullpanel(char * ip, unsigned short port, int dmxport, int direction);
    DMXPanelCollection * create_default_panels();
    DMXPanelCollection * dmxpanelcltn_create(int width, int height);
    RGBLed * dmxpanelcltn_getpixel(DMXPanelCollection * panelcltn, int row, int column);
    void dmxpanelcltn_setpanel(DMXPanelCollection * panelcltn, DMXPanel * panel, int row, int column);
    void dmxpanelcltn_sendframe(DMXPanelCollection * panelcltn);
    DMXPanel * dmxpanelcltn_getpanel(DMXPanelCollection * panelcltn, int row, int column);
    void dmxpanelcltn_wait(DMXPanelCollection * panelcltn);
    void dmxpanel_wait(DMXPanel * panel);
    void pixel_print(RGBLed * led);

    /* Destroyers */
    void ledarray_destroy(LEDArray * ledarray);
    void dmxpanel_destroy(DMXPanel * dmxpanel);
    void dmxpanelcltn_destroy(DMXPanelCollection * panelcltn);

    /* Other functions */
    int dmxpanel_sendframe(DMXPanel * panel, int usecache);

static inline RGBLed * dmxpanel_getpixel(DMXPanel * dmxpanel, SZ r, SZ c)
{
    unsigned int idx;
    unsigned int cprime = c;
    if (dmxpanel->direction) {
        cprime = dmxpanel->width - c - 1;
    }
    idx = (dmxpanel->func)(dmxpanel->height, dmxpanel->width, r, cprime);
    if (idx < 0 || idx >= dmxpanel->leds->size) {
        return (RGBLed *)0;
    }
    dmxpanel->stale = 1;
    return dmxpanel->leds->led + idx;
}


    RGBLed * pixel_setrgb(RGBLed * led, float red, float green, float blue);
    RGBLed * pixel_sethue(RGBLed * led, float hue, float brightness, float saturation);

    /* These operate such that the destination is dst.
       I.e.: dst <- dst * src
    */
    RGBLed * pixel_add(RGBLed * dst, RGBLed * src);
    RGBLed * pixel_multiply(RGBLed * dst, RGBLed * src);
#ifdef __cplusplus
}
#endif

#ifndef MIN
#define MIN(a, b) (((a) < (b)) ? (a) : (b))
#endif
#ifndef MAX
#define MAX(a, b) (((a) > (b)) ? (a) : (b))
#endif



#endif
