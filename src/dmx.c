#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <time.h>

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
    if (c < 6) {
        return r + 12 * (5 - c);
    }
    else {
        return r + 12*c;
    }
}

#define FLOAT2CHAR(A) ((unsigned char)(256 * (MIN(MAX(A, 0), 0.999))))

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
DMXPanel * dmxpanel_create(char * ip, unsigned short port, int dmxport, SZ width, SZ height, int (* mapfunc)(int, int))
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
    panel->direction = 0;

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

    panel->sockfd = -1;
    if (_dmxpanel_createsocket(panel)) {
        _ERROR("Could not create socket");
    }
    return panel;
}

DMXPanel * dmxpanel_createhalfpanel(char * ip, unsigned short port, int dmxport, int direction)
{
    DMXPanel * panel = dmxpanel_create(ip, port, dmxport, 6, 12, NULL);
    panel->direction = direction;
    return panel;
}

/*
DMXPanel * dmxpanel_createfullpanel(char * ip, unsigned short port, int dmxport, int direction)
{

}
*/


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

int dmxpanel_sendframe(DMXPanel * panel)
{
    unsigned char * ptr;
    int color_base = 24;
    int i;
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
        return 0;
    }
}


extern inline RGBLed * dmxpanel_getpixel(DMXPanel * dmxpanel, SZ x, SZ y)
{
    unsigned int idx;
    idx = (dmxpanel->func)(x, y);
    if (idx < 0 || idx >= dmxpanel->leds->size) {
        printf("%u x %u: %u\n", x, y, idx);
        _ERROR("Invalid index for leds!");
    }
    return &(dmxpanel->leds->led[idx]);
}


#ifdef DMX_TEST
int main(int argc, char ** argv)
{
    DMXPanel * panel = dmxpanel_create("TEPILEPSY.MIT.EDU", 6038, 0, 12, 12, NULL);
    int i, r, c;
    for (i = 0; i < 12 * 12; i++) {
        if (0) {
            pixel_setrgb(dmxpanel_getpixel(panel, r, c), 0, 0, 0);
        }
        r = i % 12;
        c = i / 12;
        pixel_setrgb(dmxpanel_getpixel(panel, r, c), 1, 1, 1);
        /*pixel_setrgb(dmxpanel_getpixel(panel, r, c), 1, 1, 1); */
        printf("Doing (%u, %u)\n", r, c);
    }
    dmxpanel_sendframe(panel);
    dmxpanel_destroy(panel);
        /*usleep(50000);*/

    return 0;
}
#endif
