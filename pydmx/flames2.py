#!/usr/bin/python

import dmxwidget
import math
import random

class Flames2 (dmxwidget.Widget) :
    colorstate = None
    def draw(self, panel) :
        if self.colorstate == None :
            self.colorstate = [[0.0 for pixel in row] for row in panel.lights]
        self.nextstate(self.colorstate)
        for r in range(0, panel.height) :
            for c in range(0, panel.width) :
                panel.lights[r][c].sethue(0.2-self.colorstate[r][c]*0.07,1-self.colorstate[r][c], 0.1*(1-self.colorstate[r][c]))
        panel.outputAndWait(30)

    def nextstate(self, colorstate) :
        k = 0.2
        d = 0.99999
        oldstate = [[x for x in row] for row in colorstate]
        for r in range(0, len(colorstate)) :
            for c in range(0, len(colorstate[r])) :
                count = 0
                if r > 0 :
                    s = oldstate[r-1][c]
                else :
                    s = random.random()
                if c > 0 and r > 0 :
                    s += oldstate[r-1][c-1]/2
                    count += 1
                if c + 1 < len(colorstate[r]) and r > 0:
                    s += oldstate[r-1][c+1]/2
                    count += 1
                if count > 0 :
                    s = s/(count/2+1)
                colorstate[r][c] = (k*oldstate[r][c]*d+(1-k)*s)

if __name__=="__main__" :
    ws = dmxwidget.WidgetServer()
    ws.run([Flames2])
