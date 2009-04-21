import dmx
import math

panel1 = dmx.LightPanel("18.224.3.100", 6038, 0, 0)
panel2 = dmx.LightPanel("18.224.3.102", 6038, 0, -3)
panel = dmx.PanelComposite()
panel.addPanel(panel1, 0, 12)
panel.addPanel(panel2, 0, 0)

width = 1.0

def setColor(panel, shimmer_angle, hue, x, y, lightrow, lightcol) :
    dist = math.cos(shimmer_angle/10)*x*y+math.cos(shimmer_angle)*x*x+math.sin(shimmer_angle)*y*y
    panel.lights[lightrow][lightcol].sethue(hue+dist/2.5, 1, 0)

hue = 0.0
shimmer_angle = 0.0
center_x=0.0
center_y=0.0
dx=0.001
dy=0.001

while True :
    hue+=2/255.0;
    shimmer_angle += 0.05
    center_x+=dx*math.cos(shimmer_angle/100)
    center_y+=dy*math.sin(shimmer_angle/100)
    if center_x>width :
        dx = -dx
        center_x=1.0
    elif center_x < -1 :
        dx = -dx
        center_x=-1
    if center_y>1 :
        dy = -dy
        center_y=1
    elif center_y < -1 :
        dy=-dy
        center_y=-1

    for row in range(0, panel.height) :
        for col in range(0, panel.width) :
            setColor(panel, shimmer_angle, hue, (float(col)/panel.width-0.5)*width*2-center_x, (float(row)/panel.height-0.5)*width*2-center_y, row, col)
    panel.output()
