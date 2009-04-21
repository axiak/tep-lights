import dmx

panel = dmx.LightPanel("18.224.3.100", 6038, 0)

for row in panel.lights:
    for light in row:
        light.sethue(0, 0, 0)
panel.outputAndWait(5)
