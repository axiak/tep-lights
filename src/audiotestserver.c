#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include <fftw3.h>
#include <math.h>
#include <jack/jack.h>

#include "ipcstructs.h"
#include "server.h"
#include "dmx.h"
#include "beat.h"
#include "dmxdummy.h"

double * in;
fftw_complex * out;
fftw_complex * in2;
double * out2;
fftw_plan ff_plan;
fftw_plan ff_plan2;

jack_client_t * jclient;
jack_port_t * j_lp;
jack_port_t * j_rp;


void j_shutdown(void *arg);
int j_receive(jack_nframes_t nframes, void * arg);
void analyze(void);

SoundInfo * soundinfo;

int main(int argc, char ** argv)
{
    ServerInfo * info = new_serverenvironment();
    int numc = -1, newc;
    ColorLayer * layer;
    int i, j;
    int found = 0;
    DMXDummyPanel * panel = dummypanel_create(48, 24);

    soundinfo = info->soundinfo;
    info->panel = panel->cltn;

    in = (double*) fftw_malloc(sizeof(double) * FFT_WINDOW_SIZE);
    out = (fftw_complex*) fftw_malloc(sizeof(fftw_complex) * FFT_WINDOW_SIZE);
    out2 = (double*) fftw_malloc(sizeof(double) * FFT_WINDOW_SIZE);
    in2 = (fftw_complex*) fftw_malloc(sizeof(fftw_complex) * FFT_WINDOW_SIZE);
    ff_plan = fftw_plan_dft_r2c_1d(FFT_WINDOW_SIZE, in, out, 0);
    ff_plan2 = fftw_plan_dft_c2r_1d(FFT_WINDOW_SIZE, in2, out2, 0);

    // set up jack
    printf("Connecting to jack...\n");
    if(!(jclient = jack_client_open("timbre", JackNoStartServer, NULL))) {
        fprintf(stderr, "Cannot connect to jack.\n");
        return 1;
    }
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

    ColorLayer * layer2 = colorlayer_create();

    while (1) {
        colorlayer_setall(layer2, 0, 0, 0, 1);
        info->soundinfo->frame_counter++;
        found = 0;
        newc = num_clients(info->ipcdata);
        if (newc != numc) {
            printf("Total clients: %d\n", newc);
            numc = newc;
        }
        for (i = 0; i < MAXPLUGINS; i++) {
            if (is_client_running(&info->ipcdata->plugins[i])) {
                layer = plugin_useotherlayer(info->ipcdata, i);
                //ColorLayer * colorlayer_addalpha(layer2, layer);
                plugin_disuseotherlayer(info->ipcdata, i);
                colorlayer_pushtocollection(info->panel, layer);
                break;
            }
        }

        //colorlayer_pushtocollection(info->panel, layer2);

        /*
        for (i = 0; i < 48 * 24; i++){
            RGBLed * p = dmxpanelcltn_getpixel(info->panel, i / 48, i % 48);
            pixel_print(p);
        }
        */
        /*dmxpanelcltn_sendframe(info->panel);*/
        dummypanel_sendframe(panel);
    }
    dummypanel_destroy(panel);
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
        in[i] = lin[b] + rin[b];
    }
    if(i >= FFT_WINDOW_SIZE) {
        i = 0;
        analyze();
    }
    return 0;
}


void analyze(void) {
    int i, j;

    static double band_volume[BINS_TO_USE];
    static double beat_band[BEAT_BANDS];
    static double band_history[AVG_HISTORY_LENGTH][BEAT_BANDS];
    static double deriv_history[AVG_HISTORY_LENGTH][BEAT_BANDS];
    static char beat_history[BEAT_HISTORY_LENGTH][BEAT_BANDS];
    static int place = 0;

    static char init = 0;

    if( init == 0 ) {
        for(j = 0; j < BEAT_BANDS; j++) {
            for(i = 0; i < AVG_HISTORY_LENGTH; i++)
                band_history[i][j] = deriv_history[i][j] = 0;
            for(i = 0; i < BEAT_HISTORY_LENGTH; i++)
                beat_history[i][j] = 0;
        }
        init = 1;
    }
    fftw_execute(ff_plan);

    double volume = 0;

    for(i = 0; i < BINS_TO_USE; i++) {
        soundinfo->fft[i] = band_volume[i] = pow(out[i][0], 2.0)+pow(out[i][1], 2.0);
    }
    for (; i < FFT_WINDOW_SIZE; i++) {
        soundinfo->fft[i] = pow(out[i][0], 2.0)+pow(out[i][1], 2.0);
        volume += soundinfo->fft[i];
    }
    volume /= FFT_WINDOW_SIZE;
    volume = sqrt(volume);

    for (i = 0; i < 23; i++) {
        soundinfo->volumehistory[i + 1] = soundinfo->volumehistory[i];
    }
    soundinfo->volumehistory[0] = volume;

    for(i = 0; i < BEAT_BANDS; i++) {
        int size = BINS_TO_USE/BEAT_BANDS;;
        for(j = 0; j < size; j++)
            beat_band[i] += band_volume[i*size+j];
        beat_band[i] /= (float)size;
        beat_band[i] = sqrt(beat_band[i]);
        printf("\t%f",beat_band[i]);
    }
    printf("\n");

    double avg[BEAT_BANDS];
    double var[BEAT_BANDS];

    char is_beat[BEAT_BANDS];
    for(j = 0; j < BEAT_BANDS; j++) {
        avg[j] = 0;
        for(i = 0; i < AVG_HISTORY_LENGTH; i++)
            avg[j] += deriv_history[i][j];
        avg[j] /= (float)AVG_HISTORY_LENGTH;
        var[j] = 0;
        for(i = 0; i < AVG_HISTORY_LENGTH; i++)
            var[j] += pow(deriv_history[i][j]-avg[j],2);
        var[j] /= (float)AVG_HISTORY_LENGTH;
        
        double cutoff = 1.5-.00002*var[j];
        //    printf("\tc:%f",cutoff);
        
        deriv_history[place%AVG_HISTORY_LENGTH][j] = MAX(beat_band[j]-band_history[(place-1)%AVG_HISTORY_LENGTH][j],0)*44100/FFT_WINDOW_SIZE;
        //    printf("\td:%f", deriv_history[place%AVG_HISTORY_LENGTH][j]);
        band_history[place%AVG_HISTORY_LENGTH][j] = beat_band[j];
        if(deriv_history[place%AVG_HISTORY_LENGTH][j] > 1.4/*cutoff*/*avg[j])
            is_beat[j] = 1;
        else
            is_beat[j] = 0;

        beat_history[place%BEAT_HISTORY_LENGTH][j] = is_beat[j];
        soundinfo->current_beats[j] = is_beat[j];
        printf("\t%f\t%f\t%i",avg[j],var[j],is_beat[j]);
    }
    printf("\n\n");
    place++;
    soundinfo->frame_counter++;
}
