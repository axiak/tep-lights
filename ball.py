import dmx
import math

panel = dmx.LightPanel("18.224.3.100", 6038, 0)

def setColor(panel, shimmer_angle, hue, x, y, lightrow, lightcol) :
    dist = math.cos(shimmer_angle/10)*x*y+math.cos(shimmer_angle)*x*x+math.sin(shimmer_angle)*y*y
    panel.lights[lightrow][lightcol].sethue(hue+dist/2.5, 1, 0)

def colorset(panel, hue, brightness, x, y):
    panel.lights[int(y)][int(x)].sethue(hue, brightness, 0)

def drawball(panel, x, y):
    centerhue = 0.4
    skinhue = 0.8
    colorset(panel, centerhue, 1, x, y)
    colorset(panel, skinhue, 0.6, x+1, y)
    colorset(panel, skinhue, 0.6, x-1, y)
    colorset(panel, skinhue, 0.6, x, y+1)
    colorset(panel, skinhue, 0.6, x, y-1)
    colorset(panel, skinhue, 0.2, x+1, y+1)
    colorset(panel, skinhue, 0.2, x+1, y-1)
    colorset(panel, skinhue, 0.2, x-1, y-1)
    colorset(panel, skinhue, 0.2, x-1, y+1)

def clear(panel):
    for row in panel.lights:
        for light in row:
            light.sethue(0, 0, 0)

hue = 0.0
center_x=0.0
center_y=0.0
dx=0.4
dy=0.5

while True :
    hue+=2/255.0;
    center_x+=dx
    center_y+=dy
    if center_x>(panel.width-2):
        dx = -dx
        center_x = panel.width - 2
    elif center_x<1:
        dx = -dx
        center_x = 1
    if center_y>(panel.height-2):
        dy = -dy
        center_y = panel.height - 2
    elif center_y<1:
        dy=-dy
        center_y = 1
    clear(panel)
    drawball(panel, center_x, center_y)
#    colorset(panel, hue, 1, center_x, center_y)
    panel.outputAndWait(30)
