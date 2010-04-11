#!/usr/bin/python
from cydmx import dmxwidget
import math
import random

class SurfBall (dmxwidget.Widget) :
    def init(self, panel) :
        self.hue = 0.9
        self.center_x=0.0
        self.center_y=0.0
        self.dx=0.4
        self.dy=0.5

    def draw(self, panel) :
        self.center_x+=self.dx
        self.center_y+=self.dy
        if self.center_x>(panel.width-1):
            self.dx = -self.dx #+ (0.5 - random.random())/10.
            self.center_x = panel.width - 1
        elif self.center_x<0:
            self.dx = -self.dx #+ (0.5 - random.random())/10
            self.center_x = 0
        if self.center_y>(panel.height-1):
            self.dy = -self.dy #+ (0.5 - random.random())/10
            self.center_y = panel.height - 1
        elif self.center_y<0:
            self.dy=-self.dy #+ (0.5 - random.random())/10
            self.center_y = 0
        for row in xrange(panel.height):
            for column in xrange(panel.width):
                setColor(panel, self.hue, self.center_x, self.center_y, row, column)
        panel.outputAndWait(30)

def colorset(panel, hue, brightness, x, y):
    panel.lights[int(y)][int(x)].sethue(hue, brightness, 0)

def setColor(panel, hue, x, y, row, col):
    hs = 3               # hue variance
    bs = 5               # brightness variance
    ss = 3               # saturation variance
    dist = math.sqrt((x - col)**2. + (y - row)**2)
    #panel.lights[row][col].sethue(hue/(1 + 0.4*dist), 2/(0.05 + dist), 0)
    pointhue = 2*hs*math.exp(-dist**2/(2*hs**2))/(hs*math.sqrt(2*math.pi))
    pointbrightness = 3*bs*math.exp(-dist**2/(2*bs**2))/(bs*math.sqrt(2*math.pi))
    pointsat = 1/(1+dist**2)
    #pointsat = ss*math.exp(-dist**2/(2*ss**2))/(ss*math.sqrt(2*math.pi))
    panel.lights[row][col].sethue(pointhue, pointbrightness, pointsat)

def clear(panel):
    for row in panel.lights:
        for light in row:
            light.sethue(0, 0, 0)

if __name__=="__main__" :
    dmxwidget.WidgetServer().run([SurfBall])
