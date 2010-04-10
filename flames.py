import dmxwidget
import math
import random

class Flames (dmxwidget.Widget) :
    heights = []
    def draw(self, panel) :
        if len(self.heights) != panel.width :
            self.heights = [0 for i in xrange(panel.width)]
        for col in xrange(panel.width):
            self.heights[col] += random.randint(-1, 1)
            self.heights[col] = max(min(self.heights[col], panel.height), 1)
            drawCol(panel, col, self.heights[col])
        panel.outputAndWait(30)

flamehue = 0.8

def drawCol(panel, col, top):
    for row in xrange(panel.height):
        if row > top:
            #panel.lights[row][col].sethue(0.2, 0.5, 0)
            panel.lights[row][col].sethue(0,0,0)
        else:
            panel.lights[row][col].sethue(flamehue, 1 - float(row)/top, (1-float(row)/top)**4)
def clear(panel):
    for row in panel.lights:
        for light in row:
            light.sethue(0, 0, 0)

if __name__=="__main__" :
    dmxwidget.WidgetServer().run([Flames])
