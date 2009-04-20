import dmx
import math

panel = dmx.LightPanel("18.224.3.100", 6038, 0)

while True :
    for t in range(0, 255) + range(255, 0, -1):
        for row in range(0, panel.height) :
            for col in range(0, panel.width) :
                panel.lights[row][col].sethue(col/float(panel.width), t/255.0, row/float(panel.height))
        panel.outputAndWait(30)
