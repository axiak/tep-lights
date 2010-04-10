#include <stdio.h>
#include <fftw3.h>
#include <math.h>
#include <jack/jack.h>
#include <unistd.h>
#include "dmx-eth.h"

#include "beat.h"


/*
compile with: gcc -o fft fft.c -lfftw3 -ljack -lm
gcc -o fft fft.c -I /Library/Frameworks/Jackmp.framework/Versions/Current/Headers/ -lfftw3 -ljack -lm
*/

inline float abs(float x)
{
  if(x<0)
    return -x;
  return x;
}
inline float max(float x, float y)
{
  if(x>y)
    return x;
  return y;
}

double * in;
fftw_complex * out;
fftw_complex * in2;
double * out2;
fftw_plan ff_plan;
fftw_plan ff_plan2;

jack_client_t * jclient;
jack_port_t * j_lp;
jack_port_t * j_rp;

int ck_light;
unsigned char light_data[512];

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


  for(i = 0; i < BINS_TO_USE; i++) {
    band_volume[i] = pow(out[i][0], 2.0)+pow(out[i][1], 2.0);
    
  }


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

    deriv_history[place%AVG_HISTORY_LENGTH][j] = max(beat_band[j]-band_history[(place-1)%AVG_HISTORY_LENGTH][j],0)*44100/FFT_WINDOW_SIZE;
    //    printf("\td:%f", deriv_history[place%AVG_HISTORY_LENGTH][j]);
    band_history[place%AVG_HISTORY_LENGTH][j] = beat_band[j];
    if(deriv_history[place%AVG_HISTORY_LENGTH][j] > 1.4/*cutoff*/*avg[j])
      is_beat[j] = 1;
    else
      is_beat[j] = 0;

    beat_history[place%BEAT_HISTORY_LENGTH][j] = is_beat[j];

    printf("\t%f\t%f\t%i",avg[j],var[j],is_beat[j]);
  }
  printf("\n\n");

  

  place++;
  
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
  //  if(i < FFT_WINDOW_SIZE
  //  memcpy(in, lin, sizeof(jack_default_audio_sample_t)*nframes);
  //  fftw_execute(ff_plan);

  return 0;
}

void j_shutdown(void *arg) {
  
}

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
