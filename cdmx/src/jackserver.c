#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include <time.h>
#include <sys/time.h>

#include <fftw3.h>
#include <math.h>
#include <jack/jack.h>

#include "ipcstructs.h"
#include "server.h"
#include "dmx.h"
#include "beat.h"

#ifdef TESTDUMMY
#include "dmxdummy.h"
#endif

jack_client_t * jclient;
jack_port_t * j_lp;
jack_port_t * j_rp;
int debug;

void j_shutdown(void *arg);
int j_receive(jack_nframes_t nframes, void * arg);
void analyze(void);
double _currenttime();

SoundInfo * soundinfo;

#define FPSDELAY 5

#define IFDEBUG if (debug)  

int main(int argc, char ** argv)
{
    ServerInfo * info = new_serverenvironment();
    ColorLayer * layer;
    int i;
    int frames = 0;
    double lastfpscount = _currenttime();
    double ctime;
    int foreground_plugin = 301;

#ifdef TESTDUMMY
    DMXDummyPanel * panel = dummypanel_create(60, 36);
    info->panel = panel->cltn;
#endif

    debug = 0;
    if (argc > 1) {
        for (i = 1; i < argc; i++) {
            if (!strcmp(argv[i], "-d")) {
                debug = 1;
            }
            if (atoi(argv[i])) {
                foreground_plugin = atoi(argv[i]);
            }
        }
    }
    soundinfo = info->soundinfo;


    // set up jack
    printf("Connecting to jack...\n");
    if ((jclient = jack_client_open("timbre", JackNoStartServer, NULL))) {
        printf("Connected.\n");

        jack_set_process_callback(jclient, j_receive, 0);
        jack_on_shutdown(jclient, j_shutdown, 0);
    
        printf("set jack callbacks\n");
        
        if(jack_activate(jclient)) {
            fprintf(stderr, "Cannot activate jack client.\n");
            return 1;
        }
    
        printf("activated jack client\n");
        
        j_lp = jack_port_register(jclient, "in1", JACK_DEFAULT_AUDIO_TYPE, JackPortIsInput, 0);
        j_rp = jack_port_register(jclient, "in2", JACK_DEFAULT_AUDIO_TYPE, JackPortIsInput, 0);
        
    }
    else {
        fprintf(stderr, "Could not connect to Jack client... Audio disabled!\n");
    }

    ColorLayer * shimmering = colorlayer_create();
    ColorLayer * circles = colorlayer_create();

    int gotplugin = 0;
    int background = 0;
    int pluginfound = 0;
    int num_layers = 0;
    while (1) {
        colorlayer_setall(shimmering, 0, 0, 0, 0);
        colorlayer_setall(circles, 0, 0, 0, 0);
        background = 0;
        pluginfound = 0;
        num_layers = 0;
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
            dmxpanelcltn_wait(info->panel);
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


void j_shutdown(void *arg) {
    fprintf(stderr, "Jack shut down\n");
}


int j_receive(jack_nframes_t nframes, void * arg) {
    static int i = 0;
    int b;
    jack_default_audio_sample_t *lin = (jack_default_audio_sample_t*)jack_port_get_buffer(j_lp, nframes);
    jack_default_audio_sample_t *rin = (jack_default_audio_sample_t*)jack_port_get_buffer(j_rp, nframes);
    
    for(b = 0; i < FFT_WINDOW_SIZE && b < nframes; b++, i++) {
        soundinfo->_fft_in[i] = lin[b] + rin[b];
    }
    if(i >= FFT_WINDOW_SIZE) {
        i = 0;
        soundinfo_analyze(soundinfo);
    }
    return 0;
}
