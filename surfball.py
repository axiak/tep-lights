import dmx
import math

panel = dmx.LightPanel("18.224.3.100", 6038, 0)

def colorset(panel, hue, brightness, x, y):
    panel.lights[int(y)][int(x)].sethue(hue, brightness, 0)

def setColor(panel, hue, x, y, row, col) :
    dist = math.sqrt((x - col)**2 + (y - row)**2)
    panel.lights[row][col].sethue(hue/(1 + 0.4*dist), 2/(0.05 + dist), 0)

def clear(panel):
    for row in panel.lights:
        for light in row:
            light.sethue(0, 0, 0)

hue = 0.9
center_x=0.0
center_y=0.0
dx=0.4
dy=0.5

while True :
    center_x+=dx
    center_y+=dy
    if center_x>(panel.width-1):
        dx = -dx
        center_x = panel.width - 1
    elif center_x<0:
        dx = -dx
        center_x = 0
    if center_y>(panel.height-1):
        dy = -dy
        center_y = panel.height - 1
    elif center_y<0:
        dy=-dy
        center_y = 0
    for row in xrange(panel.height):
        for column in xrange(panel.width):
            setColor(panel, hue, center_x, center_y, row, column)
    #clear(panel)
    #drawball(panel, center_x, center_y)
    #colorset(panel, hue, 1, center_x, center_y)
    panel.outputAndWait(30)
