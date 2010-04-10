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

class sPDS480caConnection :
    def __init__(self, address, universe) :
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        self.sock.connect((address, 6038))
        self.universe = universe
        self.magic = ("\x04\x01\xdc\x4a" # magic number
                      +"\x01\x00" # kk version
                      +"\x08\x01"
                      +"\x00\x00\x00\x00\x00\x00\x00\x00"
                      +chr(universe)+"\xD1\x00\x00\x00\x02\x00")

    def send_dmx(self, data) :
        self.sock.send(self.magic+data)
        # no error detection! yay!

class RGBLight :
    def __init__(self, row, col) :
        self.r = 0
        self.g = 0
        self.b = 0
        self.row = row
        self.col = col
    
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

class SimpleLights :
    def __init__(self, dmx) :
        self.lights = [[RGBLight(j, 0)] for j in range(0, 128)]
        self.dmx = dmx
        self.width = 1
        self.height = 128
        self.time = time.time()
    def output(self) :
        out = chr(0x00)
        for i in range(0,128) :
            out += chr(int(255*min(max(float(self.lights[i][0].r),0),1.0)))
            out += chr(int(255*min(max(float(self.lights[i][0].g),0),1.0)))
            out += chr(int(255*min(max(float(self.lights[i][0].b),0),1.0)))
        while(len(out)<512) :
            out += chr(0x00)
        out += chr(255)+chr(191)
        self.dmx.send_dmx(out)
    def outputAndWait(self, fps) :
        self.output()
        endtime = time.time()-self.time
        if(1.0/fps > endtime) :
            time.sleep(1.0/fps-endtime)
        self.time = time.time()
        
class LightPanel :
    def __init__(self, dmx, comp) :
        self.lights = [[RGBLight(j, i) for i in range(0,12)]
                       for j in range(0,12)]
        self.dmx = dmx
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

class HalfLightPanel :
    # direction: 0 is "bottom right corner is (0,0)" and 1 is "bottom left ..."
    def __init__(self, dmx, direction) :
        self.width = 6
        self.height = 12
        self.direction = direction
        self.lights = [[RGBLight(j, i) for i in range(0, self.width)]
                       for j in range(0, self.height)]
        self.dmx = dmx
        self.time = time.time()
    def output(self) :
        out = chr(0)
        row = 0
        col = 0
        for i in range(0, 72) :
            row = i%12
            if self.direction == 0 :
                col = 5-(i//12)
            else :
                col = i//12
            l = self.lights[row][col]
            out += chr(int(255*min(max(pow(l.r, 0.9), 0.0), 1.0)))
            out += chr(int(255*min(max(pow(l.g, 0.9), 0.0), 1.0)))
            out += chr(int(255*min(max(pow(l.b, 0.9), 0.0), 1.0)))
        for i in range(12*6, 511) :
            out += chr(0)
        out += chr(0xbf)
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
    panel = PanelComposite()
    for i in range(1,17) :
        panel_part = HalfLightPanel(sPDS480caConnection("18.224.0.194", i), 1-(i%2))
        panel.addPanel(panel_part, 12*(1-((i-1)//8)), 6*((i-1)%8))
    return panel

#def getDefaultPanel() :
#    return LightPanel(DmxConnection("18.224.1.163", 6038, 0), 0)

if __name__=="__main__" :
    a = getDefaultPanel()
    color = 1.0
    while True :
        for row in a.lights :
            for light in row :
                light.r=color
                a.outputAndWait(30)
        for row in a.lights :
            for light in row :
                light.g=color
                a.outputAndWait(30)
        for row in a.lights :
            for light in row :
                light.b=color
                a.outputAndWait(30)
        color = 1.0-color
