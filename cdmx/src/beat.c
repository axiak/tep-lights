#include <stdio.h>
#include <fftw3.h>
#include <math.h>
#include <unistd.h>
#include <string.h>

#include "beat.h"


#define MAGNITUDE(A) (pow((A)[0], 2.0) + pow((A)[1], 2.0))

static inline float max(float x, float y)
{
    if (x>y)
        return x;
    else
        return y;
}
__attribute__ ((always_inline))


/* Hann window function */
static inline double window_function(int input)
{
    return 0.5 * (1 - cos(2 * M_PI * input / (FFT_WINDOW_SIZE - 1)));
}
__attribute__ ((always_inline))


void soundinfo_init_server(SoundInfo * s)
{
    s->_fft_in = (double *) fftw_malloc(sizeof(double) * FFT_WINDOW_SIZE);
    s->_fft_out = (fftw_complex*) fftw_malloc(sizeof(fftw_complex) * FFT_WINDOW_SIZE);
    s->_fft_plan = fftw_plan_dft_r2c_1d(FFT_WINDOW_SIZE,
                                        s->_fft_in,
                                        s->_fft_out,
                                        FFTW_MEASURE);
}

void soundinfo_analyze(SoundInfo * s)
{
    register int i, j;

    static double band_volume[BINS_TO_USE];
    static double beat_band[BEAT_BANDS];
    static double band_history[AVG_HISTORY_LENGTH][BEAT_BANDS];
    static double deriv_history[AVG_HISTORY_LENGTH][BEAT_BANDS];
    static char beat_history[BEAT_HISTORY_LENGTH][BEAT_BANDS];
    static int place = 0;

    static char init = 0;

    if (init == 0) {
        memset(band_history, 0, sizeof(band_history));
        memset(deriv_history, 0, sizeof(deriv_history));
        init = 1;
    }

    for (i = 0; i < FFT_WINDOW_SIZE; i++) {
        s->_fft_in[i] *= window_function(i);
    }

    fftw_execute(s->_fft_plan);

    double volume = 0;

    for(i = 0; i < FFT_WINDOW_SIZE; i++) {
        s->fft[i] = MAGNITUDE(s->_fft_out[i + 1]);

        if (i < BINS_TO_USE)
            band_volume[i] = s->fft[i];

        volume += s->fft[i];

        if (s->fft[i] > s->short_avg[i])
            s->short_avg[i] = s->short_avg[i] * 0.2 + s->fft[i] * 0.8;
        else
            s->short_avg[i] = s->short_avg[i] * 0.5 + s->short_avg[i] * 0.5;

        if (place < 50)
            s->long_avg[i] = s->long_avg[i] * 0.9 + s->fft[i] * 0.1;
        else
            s->long_avg[i] = s->long_avg[i] * 0.992 + s->fft[i] * 0.008;

        if (fabsf(s->long_avg[i]) < 0.001) {
            s->fft_rel[i] = 1.0;
            s->avg_rel[i] = 1.0;
        }
        else {
            s->fft_rel[i] = s->fft[i] / s->long_avg[i];
            s->avg_rel[i] = s->short_avg[i] / s->long_avg[i];
        }
    }

    volume /= FFT_WINDOW_SIZE;
    volume = sqrt(volume);

    for (i = 0; i < 23; i++) {
        s->volumehistory[i + 1] = s->volumehistory[i];
    }
    s->volumehistory[0] = volume;

    for(i = 0; i < BEAT_BANDS; i++) {
        int size = BINS_TO_USE/BEAT_BANDS;
        for(j = 0; j < size; j++)
            beat_band[i] += band_volume[i*size + j];
        beat_band[i] /= (float)size;
        beat_band[i] = sqrt(beat_band[i]);
#ifdef DEBUG
        printf("\t%f",beat_band[i]);
#endif
    }
#ifdef DEBUG
    printf("\n");
#endif

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
            var[j] += pow(deriv_history[i][j]-avg[j], 2);
        var[j] /= (float)AVG_HISTORY_LENGTH;

        //double cutoff = 1.5-.00002*var[j];

        deriv_history[place%AVG_HISTORY_LENGTH][j] = max(beat_band[j]-band_history[(place-1)%AVG_HISTORY_LENGTH][j],0)*44100/FFT_WINDOW_SIZE;
        band_history[place%AVG_HISTORY_LENGTH][j] = beat_band[j];
        if(deriv_history[place%AVG_HISTORY_LENGTH][j] > 1.4/*cutoff*/*avg[j])
            is_beat[j] = 1;
        else
            is_beat[j] = 0;

        beat_history[place%BEAT_HISTORY_LENGTH][j] = is_beat[j];
        s->current_beats[j] = is_beat[j];
    }
    place++;
}


#ifdef BEATTEST
int main(int argc, char** argv) {
    // set up color kinetics
    light_data[0] = 0;
    light_data[1] = 255;

    // set up fftw
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

    j_lp = jack_port_register(jclient, "in1", JACK_DEFAULT_AUDIO_TYPE, JackPortIsInput, 0);
    j_rp = jack_port_register(jclient, "in2", JACK_DEFAULT_AUDIO_TYPE, JackPortIsInput, 0);
  
    if(jack_activate(jclient)) {
        fprintf(stderr, "Cannot activate jack client.\n");
        return 1;
    }
  
    printf("activated jack client\n");

    //  scanf("Hit enter to quit\n");
    for(;;)
        sleep(1);
  
    jack_client_close(jclient);
  
    return 0;
}
#endif
