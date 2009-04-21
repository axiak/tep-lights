import dmx
import math
import random

panel1 = dmx.LightPanel("18.224.3.100", 6038, 0, 0)
panel3 = dmx.LightPanel("18.224.3.101", 6038, 0, 0)
panel2 = dmx.LightPanel("18.224.3.102", 6038, 0, -3)
panel = dmx.PanelComposite()
panel.addPanel(panel3, 0, 0)
panel.addPanel(panel2, 0, 12)
panel.addPanel(panel1, 0, 24)

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

hue = 0.9
center_x=0.0
center_y=0.0
dx=0.4
dy=0.5

while True :
    center_x+=dx
    center_y+=dy
    if center_x>(panel.width-1):
        dx = -dx + (0.5 - random.random())/10.
        center_x = panel.width - 1
    elif center_x<0:
        dx = -dx + (0.5 - random.random())/10
        center_x = 0
    if center_y>(panel.height-1):
        dy = -dy + (0.5 - random.random())/10
        center_y = panel.height - 1
    elif center_y<0:
        dy=-dy + (0.5 - random.random())/10
        center_y = 0
    for row in xrange(panel.height):
        for column in xrange(panel.width):
            setColor(panel, hue, center_x, center_y, row, column)
    #clear(panel)
    #drawball(panel, center_x, center_y)
    #colorset(panel, hue, 1, center_x, center_y)
    panel.outputAndWait(30)
