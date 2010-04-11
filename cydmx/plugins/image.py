#!/usr/bin/env python
from cydmx import dmx
import sys
import ImageFile

fp = open(sys.argv[1], "rb");
p = ImageFile.Parser();

while 1:
	s = fp.read(1024);
	if not s:
		break
	p.feed(s);

im = p.close();


panel = dmx.getDefaultPanel()

h = len(panel.lights)
w = len(panel.lights[0])

im.thumbnail([w,h])

sz = im.size;

offx = (h- sz[0])/2
offy = (w - sz[1])/2
for row in panel.lights:
	for pixel in row:
		cp =  (pixel.col -offx)
		rp = sz[1] - (pixel.row -offy)
		if cp >= 0 and cp < sz[0] and rp >= 0 and rp < sz[1] :
			npix = im.getpixel((cp,rp))
			panel.lights[pixel.row][pixel.col].setrgb(npix[0]/255.,npix[1]/255.,npix[2]/255.)

while True:
        panel.outputAndWait(30)
