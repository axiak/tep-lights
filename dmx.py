# dmx over ethernet via python

import socket
import time

KINET_MAGIC=chr(0x04)+chr(0x01)+chr(0xdc)+chr(0x4a)
KINET_VERSION=chr(0x01)+chr(0x00)
KINET_TYPE_DMXOUT=chr(0x01)+chr(0x01)

class DmxConnection :
    def __init__(self, address, port, dmx_port) :
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        self.sock.connect((address,port))
        self.dmx_port = dmx_port

    def send_dmx(self, data) :
        out=KINET_MAGIC+KINET_VERSION+KINET_TYPE_DMXOUT
        out+=chr(0x00)+chr(0x00)+chr(0x00)+chr(0x00) #seq
        out+=chr(self.dmx_port) # dmx port number
        out+=chr(0x00) #flags
        out+=chr(0x00)+chr(0x00) # timerVal
        out+=chr(0xFF)+chr(0xFF)+chr(0xFF)+chr(0xFF) # uni
        out+=data
        if(len(out)!=self.sock.send(out)) :
            print "socket problem"
            raise SystemExit(1)

class RGBLight :
    def __init__(self, row, col) :
        self.r = 0
        self.g = 0
        self.b = 0
        self.row = row
        self.col = col

    def setrgb(self, r, g, b) :
        self.r = r
        self.g = g
        self.b = b
    
    # h,s,b are from 0 to 1
    def sethue(self, hue, brightness, saturation) :
        angle = hue*6%6.0
        brightness = min(max(float(brightness), 0.0), 1.0)
        saturation = min(max(float(saturation), 0.0), 1.0)
        if angle<2.0 :
            self.r=1
            if angle<1.0 :
                self.g = 0
                self.b = 1.0-angle
            else :
                self.g = angle-1.0
                self.b = 0
        if angle>=2.0 and angle<4.0 :
            self.g=1
            if angle<3.0 :
                self.r=3.0-angle
                self.b=0
            else :
                self.r=0
                self.b=angle-3.0
        if angle>=4.0 :
            self.b=1
            if angle<5.0 :
                self.g=5.0-angle
                self.r=0
            else :
                self.g=0
                self.r=angle-5.0
        self.r=brightness*(min(max(brightness-saturation, 0.0), 1.0)*self.r+saturation)
        self.g=brightness*(min(max(brightness-saturation, 0.0), 1.0)*self.g+saturation)
        self.b=brightness*(min(max(brightness-saturation, 0.0), 1.0)*self.b+saturation)
    def setrgb(self, red, green, blue):
        self.r = red
        self.g = green
        self.b = blue
        
class LightPanel :
    def __init__(self, address, port, dmx_port, comp) :
        self.lights = [[RGBLight(j, i) for i in range(0,12)]
                       for j in range(0,12)]
        self.dmx = DmxConnection(address, port, dmx_port)
        self.width = 12
        self.height = 12
        self.comp = comp
        self.time = time.time()
    def output(self) :
        out = chr(0x00)
        colors = [0 for i in range(0,500)]
        for c in range(0,6) :
            for r in range(0,12) :
                colors[3*(r+12*(5-c))+0]=self.lights[r][c].r
                colors[3*(r+12*(5-c))+1]=self.lights[r][c].g
                colors[3*(r+12*(5-c))+2]=self.lights[r][c].b
        for c in range(6,12) :
            for r in range(0,12) :
                colors[3*(r+12*c)+self.comp+0]=self.lights[r][c].r
                colors[3*(r+12*c)+self.comp+1]=self.lights[r][c].g
                colors[3*(r+12*c)+self.comp+2]=self.lights[r][c].b
        for i in range(0,len(colors)) :
            out+=chr(int(255*min(max(float(colors[i]),0),1.0)))
        while(len(out)<512) :
            out+=chr(0x00)
        out+=chr(255)+chr(191)
        self.dmx.send_dmx(out)

    def outputAndWait(self, fps) :
        self.output()
        endtime = time.time()-self.time
        if(1.0/fps > endtime) :
            time.sleep(1.0/fps-endtime)
        self.time = time.time()

class PanelComposite :
    def __init__(self) :
        self.panels = []
        self.panelloc = []
        self.lights = [[]]
        self.width = 0
        self.height = 0
    def addPanel(self, panel, llrow, llcol) :
        self.panels.append(panel)
        self.panelloc.append((llrow, llcol))
        self.width=max(self.width, llcol+panel.width)
        self.height=max(self.height, llrow+panel.height)
        newlights = [[RGBLight(row, col) for col in range(self.width)] for row in range(self.height)]
        for row in self.lights :
            for light in row :
                newlights[light.row][light.col] = light
        for row in panel.lights :
            for light in row :
                light.row = llrow + light.row
                light.col = llcol + light.col
                newlights[light.row][light.col] = light
        self.lights = newlights
    def output(self) :
        for panel in self.panels :
            panel.output()
    def outputAndWait(self, fps) :
        t = False
        for panel in self.panels :
            if t :
                panel.output()
            t = True
        self.panels[0].outputAndWait(fps)

def getDefaultPanel() :
    panel1 = LightPanel("18.224.3.100", 6038, 0, -3)
    panel2 = LightPanel("18.224.3.102", 6038, 0, 0)
    panel3 = LightPanel("18.224.3.103", 6038, 0, 0)
    panel4 = LightPanel("18.224.3.101", 6038, 0, 0)
    panel = PanelComposite()
    panel.addPanel(panel1,0,0)
    panel.addPanel(panel2,0,12)
    panel.addPanel(panel3,12,0)
    panel.addPanel(panel4,12,12)
    return panel

if __name__=="__main__" :
    a = getDefaultPanel()
    for row in a.lights :
        for light in row :
            light.r=1.0
            a.outputAndWait(30)
    for row in a.lights :
        for light in row :
            light.g=1.0
            a.outputAndWait(30)
    for row in a.lights :
        for light in row :
            light.b=1.0
            a.outputAndWait(30)
