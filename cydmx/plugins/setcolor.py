#!/usr/bin/python
from cydmx import dmx

import sys

color = [float(x) for x in sys.argv[1:4]]

if __name__=="__main__" :
    a = dmx.getDefaultPanel()
    for row in a.lights:
        for light in row:
            light.setrgb(*color)
    a.output()

    if len(sys.argv) <= 4:
        while True:
            a.outputAndWait(30)
