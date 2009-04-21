import dmx

panel1 = dmx.LightPanel("18.224.3.100", 6038, 0, 0)
panel2 = dmx.LightPanel("18.224.3.102", 6038, 0, -3)
panel = dmx.PanelComposite()
panel.addPanel(panel2, 0, 0)
panel.addPanel(panel1, 0, 12)

for row in panel.lights:
    for light in row:
        light.sethue(0, 0, 0)
panel.outputAndWait(5)
