import dmx
import math

panel1 = dmx.LightPanel("18.224.3.100", 6038, 0, 0)
panel2 = dmx.LightPanel("18.224.3.102", 6038, 0, -3)
panel = dmx.PanelComposite()
panel.addPanel(panel1, 0, 12)
panel.addPanel(panel2, 0, 0)

while True :
    for t in range(0, 255) + range(255, 0, -1):
        for row in range(0, panel.height) :
            for col in range(0, panel.width) :
                panel.lights[row][col].sethue(col/float(panel.width), t/255.0, row/float(panel.height))
        panel.outputAndWait(30)
