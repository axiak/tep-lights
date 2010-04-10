#!/usr/bin/python
import dmx
import sys
import Image
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

scaling, image = sys.argv[1:]

def show_image(a):
    c = StringIO.StringIO(image.decode('base64'))
    im = Image.open(c)
    if im.mode != 'RGB':
        im = im.convert('RGB')
    box = (a.width, a.height)
    if scaling.lower() == 'resize':
        im = im.resize(box, Image.ANTIALIAS)
    elif scaling.lower() == 'thumbnail':
        im.thumbnail(box, Image.ANTIALIAS)
    else:
        raise ValueError("Invalid scaling %s" % scaling)

    height = a.height
    for row in a.lights:
        for light in row:
            impixel = im.getpixel((light.col, height - light.row - 1))
            light.setrgb(
                impixel[0] / 255.0, impixel[1] / 255.0, impixel[2] / 255.0
                )

if __name__=="__main__" :
    a = dmx.getDefaultPanel()
    show_image(a)
    a.output()
