#!/usr/bin/python
import dmx
import psyco
import sys
psyco.full()

color = [float(x) for x in sys.argv[1:]]

if __name__=="__main__" :
    a = dmx.getDefaultPanel()
    for row in a.lights:
        for light in row:
            light.setrgb(*color)
    a.output()
