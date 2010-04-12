#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include <time.h>
#include <sys/time.h>

#include <fftw3.h>
#include <math.h>
#include <pulse/simple.h>
#include <pulse/error.h>
#include <pthread.h>

#include "ipcstructs.h"
#include "server.h"
#include "dmx.h"
#include "beat.h"

#ifdef TESTDUMMY
#include "dmxdummy.h"
#endif


int debug;

double _currenttime();

SoundInfo * soundinfo;

#define FPSDELAY 5

#define IFDEBUG if (debug)  

void * pulse_handler(void * arg);

int main(int argc, char ** argv)
{
    ServerInfo * info = new_serverenvironment();
    ColorLayer * layer;
    int i;
    int frames = 0;
    double lastfpscount = _currenttime();
    double ctime;
    int pulseaudio = 0;
    pthread_t pathread;
    char * dev = "alsa_output.pci-0000_00_14.2.analog-stereo.monitor";
    if (argc > 1) {
        dev = argv[1];
    }

#ifdef TESTDUMMY
    DMXDummyPanel * panel = dummypanel_create(60, 36);
    info->panel = panel->cltn;
#endif

    soundinfo = info->soundinfo;

    if (pthread_create(&pathread, NULL, pulse_handler, (void *)dev)) {
        fprintf(stderr,
                "Could not start thread!\n");
        exit(2);
    }

    ColorLayer * shimmering = colorlayer_create();
    ColorLayer * circles = colorlayer_create();

    int gotplugin = 0;
    int background = 0;
    int pluginfound = 0;
    int num_layers = 0;
    for (;;) {
        colorlayer_setall(shimmering, 0, 0, 0, 0);
        colorlayer_setall(circles, 0, 0, 0, 0);
        background = 0;
        pluginfound = 0;
        num_layers = 0;

        if (!pulseaudio)
            info->soundinfo->frame_counter++;

        for (i = 0; i < MAXPLUGINS; i++) {
            if (is_client_running(&info->ipcdata->plugins[i])) {
                layer = plugin_useotherlayer(info->ipcdata, i);
                if (pluginfound) {
                    if (!colorlayer_mult(circles, layer)) {
                        printf("Bad plugin! '%s'\n", info->ipcdata->plugins[i].name);
                        continue;
                    }                        
                }
                else {
                    if (!colorlayer_copy(circles, layer)) {
                        printf("Bad plugin! '%s'\n", info->ipcdata->plugins[i].name);
                        continue;
                    }
                }
                num_layers ++;
                pluginfound = 1;
                gotplugin = 1;
                plugin_disuseotherlayer(info->ipcdata, i);
            }
        }
        if (!gotplugin) {
            continue;
        }

        colorlayer_pushtocollection(info->panel, circles);


#ifdef TESTDUMMY
        dummypanel_sendframe(panel);
#else
        dmxpanelcltn_sendframe(info->panel);
#endif

        frames ++;
        ctime = _currenttime();
        if ((ctime - lastfpscount) > FPSDELAY) {
            fprintf(stderr, "Num plugins: %d\n", num_layers);
            fprintf(stderr, "Frames per second: %0.3f\n",
                    frames / (ctime - lastfpscount));
            frames = 0;
            lastfpscount = ctime;
        }
    }

#ifdef TESTDUMMY
    dummypanel_destroy(panel);
#endif
    destroy_serverenvironment(info);
    return 0;
}

void * pulse_handler(void * arg)
{
    int i, error;
    uint16_t buf[FFT_WINDOW_SIZE];
    pa_simple * s;
    char * dev = (char *)arg;
    pa_sample_spec ss = {
        .format = PA_SAMPLE_S16LE,
        .rate = 16000,
        .channels = 1
    };

    // set up audio
    printf("Connecting to pulseaudio...\n");
    if (!(s = pa_simple_new(NULL, "lightbeat", PA_STREAM_RECORD, dev, "record", &ss, NULL, NULL, &error))) {
        fprintf(stderr,
                "Pulseaudio initialization failed. Perhaps you should pass "
                "in a pulseaudio device? Hint: `pactl list | grep monitor`\n");
        fprintf(stderr, "Error: %s\n", pa_strerror(error));
        return NULL;
    }
    for (;;) {
        if (pa_simple_read(s, buf, sizeof(buf), &error) < 0) {
            fprintf(stderr, "Could not read pulseaudio data: %s\n", pa_strerror(error));
            exit(1);
        }
        for (i = 0; i < FFT_WINDOW_SIZE; i++) {
            soundinfo->_fft_in[i] = (double)buf[i] / ((double)(SHRT_MAX + 1));
        }
        soundinfo_analyze(soundinfo);
    }
    if (s)
        pa_simple_free(s);
}
