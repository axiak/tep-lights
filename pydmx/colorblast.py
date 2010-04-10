import dmx
import time

class ColorBlast (dmx.LightPanel) :
    def __init__(self, address, port, dmx_port, dmx_base_channel) :
        self.lights = [[dmx.RGBLight(0, 0)]]
        self.dmx = dmx.DmxConnection(address, port, dmx_port)
        self.width = 1
        self.height = 1
        self.dmxchannel = dmx_base_channel
        self.time = time.time()
    def output(self) :
        out = chr(0x00)
        colors = [0, 0, 0]
        colors[0] = self.lights[0][0].r
        colors[1] = self.lights[0][0].g
        colors[2] = self.lights[0][0].b
        for i in range(0, self.dmxchannel) :
            out += chr(0x00)
        for i in range(0,len(colors)) :
            out+=chr(int(255*min(max(float(colors[i]),0),1.0)))
        while(len(out)<512) :
            out+=chr(0x00)
        out+=chr(255)+chr(191)
        self.dmx.send_dmx(out)

panel = ColorBlast("18.224.3.3", 6038, 0, 0)

def colorcycle(panel) :
    strobe = True
    color = 0
    while True :
        color += 0.005
        for row in panel.lights :
            for pixel in row :
                if strobe :
                    pixel.sethue(color, 1, 0.5)
                else :
                    pixel.sethue(color, 0, 0)
        #strobe = not strobe
        panel.outputAndWait(30)

panel.lights[0][0].setrgb(1.0, 1.0, 0.6)
panel.outputAndWait(30)

colorcycle(panel)
