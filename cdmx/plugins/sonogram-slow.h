#ifndef __SONOGRAM_H
#define __SONOGRAM_H 1

typedef struct CircleBuf_s {
    struct CircleBuf_s * prev;
    double * data;
} CircleBuf;

CircleBuf * circlebuf_create(int rows, int cols);
void circlebuf_destroy(CircleBuf * c);

#endif
