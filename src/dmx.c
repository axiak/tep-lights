#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h> 

#include "dmx.h"

int _dmxpanel_createsocket(DMXPanel * panel);
static inline int _dmxpanel_senddata(DMXPanel * panel, char * output, int len);

static inline void _ERROR(char * s) {
    fprintf(stderr, "%s\n", s);
    exit(2);
}

/* Default map function */
int ledmap_default(int r, int c)
{
    return r + 12 * (5 - c);
}


/* RGBLed stuff */
RGBLed * pixel_setrgb(RGBLed * led, unsigned char red, unsigned char green, unsigned char blue)
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
DMXPanel * dmxpanel_create(char * ip, unsigned short port, int dmxport, SZ width, SZ height, ledmap * mapfunc)
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

    bufsize = 26 + MAX(3 * width * height, 512) + 2;
    panel->netbuffer = (char *)malloc(bufsize);
    if (!panel->netbuffer) {
        _ERROR("Unable to allocate memory for network buffer.");
    }
    memset(panel->netbuffer, 0, bufsize);
    strcpy(panel->netbuffer,
           "\x04\x01\xdc\x4a"
           "\x01\x00"
           "\x08\x01"
           "\x00\x00\x00\x00\x00\x00\x00\x00"
           "\x00"
           "\xd1\x00\x00\x00\x02\x00"
           "\x00");
    panel->netbuffer[16] = (char)dmxport;

    if (mapfunc) {
        panel->func = mapfunc;
    }
    else {
        panel->func = (ledmap *)ledmap_default;
    }

    panel->leds = ledarray_create(width * height);

    panel->sockfd = -1;
    if (_dmxpanel_createsocket(panel)) {
        _ERROR("Could not create socket");
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

void dmxpanel_sendframe(DMXPanel * panel)
{
    char * ptr;
    int color_base = 25;

    
}



extern inline RGBLed * dmxpanel_getpixel(DMXPanel * dmxpanel, SZ x, SZ y)
{
    unsigned int idx;
    idx = (*(dmxpanel->func))(x, y);
    if (idx < 0 || idx >= dmxpanel->leds->size) {
        _ERROR("Invalid index for leds!");
    }
    return &(dmxpanel->leds->led[idx]);
}



#ifdef DMX_TEST
int main(int argc, char ** argv)
{
    printf("TEST %s\n", "\x41");
    return 0;
}
#endif
