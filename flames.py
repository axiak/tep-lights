import dmx
import math
import random

panel1 = dmx.LightPanel("18.224.3.100", 6038, 0, 0)
panel2 = dmx.LightPanel("18.224.3.101", 6038, 0, 0)
panel3 = dmx.LightPanel("18.224.3.102", 6038, 0, -3)
panel = dmx.PanelComposite()
panel.addPanel(panel3, 0, 0)
panel.addPanel(panel1, 0, 12)
panel.addPanel(panel2, 0, 24)

flamehue = 0.8

def drawCol(panel, column, top):
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

heights = [0 for i in xrange(panel.width)]

while True :
    for col in xrange(panel.width):
        heights[col] += random.randint(-1, 1)
        heights[col] = max(min(heights[col], panel.height), 1)
        drawCol(panel, col, heights[col])
    panel.outputAndWait(30)
