import dmx
import math
#import random
import datetime

panel = dmx.LightPanel("18.224.3.100", 6038, 0)

rimhue = 1
secondshue = 0.9
minuteshue = 0.5
hourshue = 0.1

centerx = (panel.width-1)/2.
centery = (panel.height-1)/2.

def drawClock(panel, hours, mins, secs):
    for x in xrange(panel.width):
        for y in xrange(panel.height):
            #rim
            if math.sqrt((x-centerx)**2 + (y-centery)**2) >= min(panel.width, panel.height)/2.:
                panel.lights[x][y].sethue(rimhue, 0.5, 0)
            #seconds
            elif math.fabs(math.degrees((math.atan2(centerx-x, y-centery))) + 90 - 6*secs) <= 7:
                panel.lights[x][y].sethue(secondshue, 1, 0)
            elif math.fabs(math.degrees((math.atan2(x-centerx, centery-y))) + 270 - 6*secs) <= 7:
                panel.lights[x][y].sethue(secondshue, 1, 0)
            #minutes
            elif math.fabs(math.degrees((math.atan2(centerx-x, y-centery))) + 90 - 6*mins) <= 7:
                panel.lights[x][y].sethue(minuteshue, 1, 0)
            elif math.fabs(math.degrees((math.atan2(x-centerx, centery-y))) + 270 - 6*mins) <= 7:
                panel.lights[x][y].sethue(minuteshue, 1, 0)
            #hours
            elif math.fabs(math.degrees((math.atan2(centerx-x, y-centery))) + 90 - 15*hours) <= 7:
                panel.lights[x][y].sethue(hourshue, 1, 0)
            elif math.fabs(math.degrees((math.atan2(x-centerx, centery-y))) + 270 - 15*hours) <= 7:
                panel.lights[x][y].sethue(hourshue, 1, 0)
            elif math.fabs(x - centerx) < 1 and math.fabs(y - centery) < 1:
                panel.lights[x][y].sethue(rimhue, 0.75, 0)
            else:
                panel.lights[x][y].sethue(0, 0, 0)
            
            
while True :
    t = datetime.datetime.now().timetuple()
    print "===", t[5], "==="
    drawClock(panel, t[3], t[4], t[5])
    panel.outputAndWait(10)
