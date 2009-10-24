#include <stdio.h>
#include <plugin.h>

#define PLUGINID 22

int main(int argc, char **argv)
{
    int i, r, c, j;
    LocalData * s = plugin_register(argv[0], PLUGINID);
    ColorLayer * layer = s->layer;
    ColorLayer * layer2;
    i = 0;
    layer->width = 48;
    layer->height = 24;

    lastUpdate = getTime();
    float speed = 6;

    float y1[20]; float y2[20]; float x1[20]; float x2[20];
    while (1) {
      serverdata_update(s); /* Wait for audio info to update */
      
      current = getTime();
      
      char* beats = s->soundinfo->current_beats;
      
      if(beats[0]) {
	i = 0;
	while(y1[i] != -1) i++;
	y1[i] = 0;
      }
      if(beats[1]) {
	i = 0;
	while(y2[i] != -1) i++;
	y2[i] = 0;
      }
      if(beats[2]) {
	i = 0;
	while(x1[i] != -1) i++;
	x1[i] = 0;
      }
      if(beats[3]) {
	i = 0;
	while(x2[i] != -1) i++;
	x2[i] = 0;
      }
      for(i = 0; i < 20; i++) {
	float d = (current-lastUpdate)*speed;
	
	if(y1[i] != -1) {
	  y1[i]+=d;
	  if(y1[i] > 23)
	    y1[i] = -1;
	  else
	    draw_gradient2(layer,0,0,&BLACK,0,y1[i],&GREEN);
	}
	if(y2[i] != -1){
	  y2[i]-=d; 
	  if(y1[i] < 0)
	    y2[i] = -1;
	  else
	    draw_gradient2(layer,0,0,&BLACK,0,y2[i],&BLUE);
	}
	if(x1[i] != -1){
	  x1[i]+=d;
	  if(y1[i] > 47)
	    x1[i] = -1;
	  else
	    draw_gradient2(layer,0,0,&BLACK,x1[i],0,&RED);
	}
	if(x2[i] != -1){
	  x2[i]-=d;
	  if(y1[i] < 0)
	    x2[i] = -1;
	  else
	    draw_gradient2(layer,0,0,&BLACK,x2[i],0,&ORANGE);
	}
      }
 
      /* Commit the layer */
      serverdata_commitlayer(s);
    }

    serverdata_destroy(s);
    return 0;
}

