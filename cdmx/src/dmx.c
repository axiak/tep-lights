#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define __USE_XOPEN_EXTENDED 500 /* Or: #define _BSD_SOURCE */
#include <unistd.h>

#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h> 

#include <sys/time.h>
#include <time.h>

#include "dmx.h"


#define INTERFRAME 0.0332

int _dmxpanel_createsocket(DMXPanel * panel);
static inline int _dmxpanel_senddata(DMXPanel * panel, char * output, int len);
double _currenttime();

static inline void _ERROR(char * s) {
    fprintf(stderr, "%s\n", s);
    exit(2);
}

/* Default map function */
int ledmap_default(int height, int width, int r, int c)
{
    if (c < 6) {
        return r + 12 * (5 - c);
    }
    else {
        return r + 12*c;
    }
}

#ifndef FLOAT2CHAR
#define FLOAT2CHAR(A) ((unsigned char)(256 * (MIN(MAX(A, 0), 0.999))))
#endif

/* RGBLed stuff */
RGBLed * pixel_setrgb(RGBLed * led, float red, float green, float blue)
{
    led->red = red;
    led->green = green;
    led->blue = blue;
    return led;
}

RGBLed * pixel_sethue(RGBLed * led, float hue, float brightness, float saturation)
/* Great "hsv" algorithm from kmill... */
{
    hue *= 6;
    float angle = ((int)hue % 6) + (hue - (int)hue);

    brightness = MIN(MAX(brightness, 0), 1);
    saturation = MIN(MAX(saturation, 0), 1);

    if (angle < 2) {
        led->red = 1;
        if (angle < 1) {
            led->green = 0;
            led->blue = 1 - angle;
        }
        else {
            led->green = angle - 1;
            led->blue = 0;
        }
    }
    if (angle >= 2 && angle < 4) {
        led->green = 1;
        if (angle < 3) {
            led->red = 3 - angle;
            led->blue = 0;
        }
        else {
            led->red = 0;
            led->blue = angle - 3;
        }
    }
    if (angle >= 4) {
        led->blue = 1;
        if (angle < 5) {
            led->green = 5 - angle;
            led->red = 0;
        }
        else {
            led->green = 0;
            led->red = angle - 5;
        }
    }

    led->red = brightness * (MIN(MAX(brightness - saturation, 0.0), 1.0) *
                             led->red + saturation);
    led->green = brightness * (MIN(MAX(brightness - saturation, 0.0), 1.0) *
                             led->green + saturation);
    led->blue = brightness * (MIN(MAX(brightness - saturation, 0.0), 1.0) *
                             led->blue + saturation);
    return led;
}

RGBLed * pixel_add(RGBLed * dst, RGBLed * src)
{
    dst->red = MAX(dst->red + src->red, 1.0);
    dst->green = MAX(dst->green + src->green, 1.0);
    dst->blue += MAX(dst->blue + src->blue, 1.0);
    return dst;
}

RGBLed * pixel_multiply(RGBLed * dst, RGBLed * src)
{
    dst->red *= src->red;
    dst->green *= src->green;
    dst->blue *= src->blue;
    return dst;
}


/* LEDArray stuff */
LEDArray * ledarray_create(SZ size)
{
    LEDArray * la;
    la = (LEDArray *)malloc(sizeof(LEDArray));
    if (!la) {
        _ERROR("Could not get memory for LEDArray!");
    }
    la->size = size;
    la->led = (RGBLed *)calloc(size, sizeof(RGBLed));
    if (!la->led) {
        _ERROR("Could not get memory for LEDArray!");
    }
    return la;
}

void ledarray_destroy(LEDArray * ledarray)
{
    if (!ledarray)
        return;
    if (ledarray->led) {
        free(ledarray->led);
    }
    free(ledarray);
}



/* DMX Stuff */
DMXPanel * dmxpanel_create(char * ip, unsigned short port, int dmxport, SZ width, SZ height, int (* mapfunc)(int, int, int, int))
{
    DMXPanel * panel;
    int bufsize;

    if (dmxport > 255 || dmxport < 0) {
        _ERROR("Invalid dmxport: Has to be between 0 and 255");
    }

    panel = (DMXPanel *)malloc(sizeof(DMXPanel));
    if (!panel) {
        _ERROR("Could not allocate memory for panel");
    }
    panel->ip = ip;
    panel->width = width;
    panel->height = height;
    panel->port = port;
    panel->dmxport = (unsigned char)dmxport;
    panel->direction = 1 - dmxport % 2;
    panel->stale = 1;
    panel->lastupdate = 0;
    bufsize = MAX(1024, 26 + MAX(3 * width * height, 512) + 2);
    panel->netbuffer = (unsigned char *)malloc(bufsize);
    if (!panel->netbuffer) {
        _ERROR("Unable to allocate memory for network buffer.");
    }
    memset(panel->netbuffer, 0, bufsize);
    memcpy(panel->netbuffer,
           "\x04\x01\xdc\x4a"
           "\x01\x00"
           "\x08\x01"
           "\x00\x00\x00\x00\x00\x00\x00\x00"
           "\x00"
           "\xd1\x00\x00\x00\x02\x00"
           "\x00", 24);

    panel->netbuffer[16] = (unsigned char)dmxport;

    if (mapfunc) {
        panel->func = mapfunc;
    }
    else {
        panel->func = &ledmap_default;
    }

    panel->leds = ledarray_create(width * height);

    if (ip) {
        panel->sockfd = -1;
        if (_dmxpanel_createsocket(panel)) {
            _ERROR("Could not create socket");
        }
    }
    return panel;
}

void dmxpanel_destroy(DMXPanel * panel)
{
    if (!panel) {
        return;
    }
    if (panel->leds) {
        ledarray_destroy(panel->leds);
    }
    if (panel->netbuffer) {
        free(panel->netbuffer);
    }
    if (panel->server_addr) {
        free(panel->server_addr);
    }
    free(panel);
}


int _dmxpanel_createsocket(DMXPanel * panel)
{
    int sockfd;
    struct sockaddr_in * server_addr = (struct sockaddr_in *)malloc(sizeof(struct sockaddr_in));
    struct hostent *server;

    sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd < 0) {
        _ERROR("Could not open socket");
    }

    server = gethostbyname(panel->ip);
    if (server == NULL) {
        _ERROR("No such hostname");
    }

    server_addr->sin_family = AF_INET;
    server_addr->sin_port = htons(panel->port);
    server_addr->sin_addr = *((struct in_addr *)server->h_addr_list[0]);
    memset(&(server_addr->sin_zero), 0, 8);

    panel->sockfd = sockfd;
    panel->server_addr = (struct sockaddr *)server_addr;
    return 0;
}


static inline int _dmxpanel_senddata(DMXPanel * panel, char * output, int len)
{
    return sendto(panel->sockfd, output, len, 0, panel->server_addr, sizeof(struct sockaddr));
}


void dmxpanel_wait(DMXPanel * panel)
{
    double future = panel->lastupdate + INTERFRAME;
    double current_time = _currenttime();
    while (future > current_time) {
        usleep((int)(((future - current_time) * 1000000)) + 10);
        current_time = _currenttime();
    }
    panel->lastupdate = current_time;
}

int dmxpanel_sendframe(DMXPanel * panel, int usecache)
{
    unsigned char * ptr;
    int color_base = 24;
    int i;

    if (usecache && !panel->stale) {
        panel->lastupdate = _currenttime();
        return 0;
    }
    ptr = panel->netbuffer + color_base;

    for (i = 0; i < panel->leds->size; i++) {
        *(ptr ++) = FLOAT2CHAR(panel->leds->led[i].red);
        *(ptr ++) = FLOAT2CHAR(panel->leds->led[i].green);
        *(ptr ++) = FLOAT2CHAR(panel->leds->led[i].blue);
    }
    /*panel->netbuffer[25 + 512] = 255;*/
    panel->netbuffer[679] = 191;

    i = 680;

    if (_dmxpanel_senddata(panel, (char *)panel->netbuffer, i) != i) {
        return 1;
    }
    else {
        panel->lastupdate = _currenttime();
        panel->stale = 0;
        return 0;
    }
}


DMXPanelCollection * dmxpanelcltn_create(int width, int height)
{
    DMXPanelCollection * cltn = (DMXPanelCollection *)malloc(sizeof(DMXPanelCollection));
    if (!cltn) {
        _ERROR("Could not allocate memory for DMXPanelCollection");
    }
    cltn->panels = (DMXPanel **)calloc(width * height, sizeof(DMXPanel *));
    if (!cltn->panels) {
            _ERROR("Could not allocate memory for DMXPanelCollection");
    }
    cltn->_ledwidth = 0;
    cltn->_ledheight = 0;
    cltn->width = width;
    cltn->height = height;
    return cltn;
}

RGBLed * dmxpanelcltn_getpixel(DMXPanelCollection * cltn, int row, int column)
/* This is the function that actually figures out which
   panel to use.
*/
{
    DMXPanel * ptr = NULL;
    int i, j;
    for (i = 0; i < cltn->width; i++) {
        for (j = 0; j < cltn->height; j++) {
            ptr = dmxpanelcltn_getpanel(cltn, j, i);
            if (ptr) {
                break;
            }
        }
        if (ptr) {
            break;
        }
    }

    i = row / ptr->height;
    j = column / ptr->width;
    ptr = dmxpanelcltn_getpanel(cltn, i, j);

    if (ptr) {
        return dmxpanel_getpixel(ptr, row % (ptr->height), column % (ptr->width));
    }
    return NULL;
}

void dmxpanelcltn_setpanel(DMXPanelCollection * panelcltn, DMXPanel * panel, int row, int column)
{
    int x = row * panelcltn->width + column;

    panelcltn->panels[x] = panel;
    panelcltn->_ledwidth = 0;
    panelcltn->_ledheight = 0;
}

void dmxpanelcltn_sendframe(DMXPanelCollection * panelcltn)
{
    int i;
    int waited = 0;
    int max = panelcltn->width * panelcltn->height;
    for (i=0; i < max; i++) {
        if (panelcltn->panels[i]) {
            if (!waited) {
                dmxpanel_wait(panelcltn->panels[i]);
                waited = 1;
            }
            dmxpanel_sendframe(panelcltn->panels[i], 1);
        }
    }
}

void dmxpanelcltn_wait(DMXPanelCollection * panelcltn)
{
    int i;
    int max = panelcltn->width * panelcltn->height;
    for (i=0; i < max; i++) {
        if (panelcltn->panels[i]) {
            dmxpanel_wait(panelcltn->panels[i]);
            break;
        }
    }
}

DMXPanel * dmxpanelcltn_getpanel(DMXPanelCollection * panelcltn, int row, int column)
{
    int x = row * panelcltn->width + column;
    return panelcltn->panels[x];
}

void dmxpanelcltn_destroy(DMXPanelCollection * panelcltn)
{
    if (!panelcltn) {
        return;
    }
    if (panelcltn->panels) {
        free(panelcltn->panels);
    }
    free(panelcltn);
}


void dmxpanelcltn_destroypanels(DMXPanelCollection * cltn)
{
    int i = cltn->width * cltn->height;
    for (; i >=  0; i--) {
        if (cltn->panels[i]) {
            dmxpanel_destroy(cltn->panels[i]);
            cltn->panels[i] = NULL;
        }
    }
}


DMXPanelCollection * create_default_panels()
{
    DMXPanelCollection * cltn;
    DMXPanel * ptr;
    int i;
    char * IPS[3] = {"TEPILEPSY.MIT.EDU",
                     "TEPILEPSY2.MIT.EDU",
                     0};

    cltn = dmxpanelcltn_create(15, 3);
    for (i = 0; i < 30; i++) {
        ptr = dmxpanel_create(
                              IPS[i / 16],
                              6038,
                              (i & 15) + 1,
                              6,
                              12,
                              NULL);
        dmxpanelcltn_setpanel(cltn, ptr, (29 - i) / 10, i % 10);
    }
    return cltn;
}


double _currenttime()
/* Get the current time... */
{
    struct timeval tv[1];

    gettimeofday(tv, 0);
    double seconds = ((double)tv->tv_sec);
    seconds += (double)(tv->tv_usec) / 1000000.0;
    return seconds;
}

void pixel_print(RGBLed * led)
{
    if (led->red > 0.001 || led->green > 0.001 || led->blue > 0.001) {
        printf("RGBLed[%0.4f,%0.4f,%0.4f]\n",
               led->red,
               led->green,
           led->blue);
    }

}


#ifdef DMX_TEST
int main(int argc, char ** argv)
{
    DMXPanelCollection * cltn = create_default_panels();
    int i;
    int r, c;

    dmxpanelcltn_sendframe(cltn);
    for (i = 0; i < 24 * 48; i++) {
        r = i / 48;
        c = i % 48;
        pixel_setrgb(
                     dmxpanelcltn_getpixel(cltn, r, c),
                     1, 0, 0);
        dmxpanelcltn_sendframe(cltn);
    }

    for (i = 0; i < 24 * 48; i++) {
        r = i / 48;
        c = i % 48;
        pixel_setrgb(
                     dmxpanelcltn_getpixel(cltn, r, c),
                     0, 1, 0);
        dmxpanelcltn_sendframe(cltn);
    }
    for (i = 0; i < 24 * 48; i++) {
        r = i / 48;
        c = i % 48;
        pixel_setrgb(
                     dmxpanelcltn_getpixel(cltn, r, c),
                     0, 0, 1);
        dmxpanelcltn_sendframe(cltn);
    }

    dmxpanelcltn_destroypanels(cltn);
    dmxpanelcltn_destroy(cltn);
    return 0;
}


#endif
