import dmx

panel = dmx.getDefaultPanel()
for row in panel.lights:
    for light in row:
        light.sethue(0, 0, 0)
panel.outputAndWait(5)
