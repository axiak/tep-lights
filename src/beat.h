#define FFT_WINDOW_SIZE 1024
#define BEAT_BANDS 4
#define BINS_TO_USE 24
#define AVG_HISTORY_LENGTH 100
#define BEAT_HISTORY_LENGTH 250

typedef struct {
  float fft[FFT_WINDOW_SIZE];
  float volumehistory[24];
  char current_beats[BEAT_BANDS];
  unsigned char bpm;
  float bpm_certainty;
  unsigned long frame_counter;
} SoundInfo;
