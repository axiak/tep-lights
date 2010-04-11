#!/usr/bin/python

from cydmx import dmxwidget
import math
import datetime

class Clock (dmxwidget.Widget) :
    def draw(self, panel) :
        global centerx, centery
        centerx = (panel.width-1)/2.
        centery = (panel.height-1)/2.

        t = datetime.datetime.now().timetuple()
        drawClock(panel, t[3], t[4], t[5])
        panel.outputAndWait(3)

rimhue = 1
secondshue = 0.9
minuteshue = 0.5
hourshue = 0.1


def drawClock(panel, hours, mins, secs):
    print hours, mins, secs
    h = (hours + 1/60.*mins)%12
    m = mins + 1/60*secs
    for x in xrange(panel.width):
        for y in xrange(panel.height):
            #rim
            if math.sqrt((x-centerx)**2 + (y-centery)**2) >= min(panel.width, panel.height)/2.:
                panel.lights[y][x].sethue(rimhue, 0.5, 0) 

            #hours
            elif math.fabs(math.degrees((math.atan2(centerx-x, y-centery))) + 90 - 30*h) <= 5:
                panel.lights[y][x].sethue(hourshue, 1, 0)
            elif math.fabs(math.degrees((math.atan2(x-centerx, centery-y))) + 270 - 30*h) <= 5:
                panel.lights[y][x].sethue(hourshue, 1, 0)

            #minutes
            elif math.fabs(math.degrees((math.atan2(centerx-x, y-centery))) + 90 - 6*m) <= 5:
                panel.lights[y][x].sethue(minuteshue, 1, 0)
            elif math.fabs(math.degrees((math.atan2(x-centerx, centery-y))) + 270 - 6*m) <= 5:
                panel.lights[y][x].sethue(minuteshue, 1, 0)

            #seconds
            elif math.fabs(math.degrees((math.atan2(centerx-x, y-centery))) + 90 - 6*secs) <= 5:
                panel.lights[y][x].sethue(secondshue, 1, 0)
            elif math.fabs(math.degrees((math.atan2(x-centerx, centery-y))) + 270 - 6*secs) <= 5:
                panel.lights[y][x].sethue(secondshue, 1, 0)

            #center blob
            elif math.fabs(x - centerx) < 1 and math.fabs(y - centery) < 1:
                panel.lights[y][x].sethue(rimhue, 0.75, 0)
            else:
                panel.lights[y][x].sethue(0, 0, 0)
            

if __name__=="__main__" :
    dmxwidget.WidgetServer().run([Clock])
