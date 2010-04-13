#ifndef __BEAT_H
#define __BEAT_H
#include <fftw3.h>

#ifndef M_PI
# define M_PI		3.14159265358979323846	/* pi */
#endif

#define FFT_WINDOW_SIZE 1024
#define BEAT_BANDS 4
#define BINS_TO_USE 36
#define AVG_HISTORY_LENGTH 100
#define BEAT_HISTORY_LENGTH 250

typedef struct {
    double fft[FFT_WINDOW_SIZE];
    double short_avg[FFT_WINDOW_SIZE];
    double long_avg[FFT_WINDOW_SIZE];
    double fft_rel[FFT_WINDOW_SIZE];
    double avg_rel[FFT_WINDOW_SIZE];
    double volumehistory[24];
    char current_beats[BEAT_BANDS];
    unsigned char bpm;
    float bpm_certainty;
    unsigned long frame_counter;
    double * _fft_in;
    fftw_complex * _fft_out;
    fftw_plan _fft_plan;
} SoundInfo;

void 
soundinfo_init_server(SoundInfo * s);
void soundinfo_analyze(SoundInfo * s);

#endif
