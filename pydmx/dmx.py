# dmx over ethernet via python

import socket
import time
import array
import struct
import functools
import numpy
try:
    import numpy
except ImportError:
    numpy = False

def _numpy_badness(*args, **kwargs):
    raise RuntimeError("Need numpy here")

def numpycheck(method):
    if numpy:
        return method
    else:
        return _numpy_badness


class sPDS480caConnection(object):
    def __init__(self, address, universe) :
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        self.sock.connect((address, 6038))
        self.universe = universe
        self.magic = struct.pack('<IHHIIBHHH',
                                 1255932164, 1, 264,
                                 0, 0, universe, 
                                 209, 0, 2)

    def send_dmx(self, data) :
        self.sock.send(self.magic + data)
        # no error detection! yay!



class RGBLight(object):
    __slots__ = ('r', 'g', 'b', 'panel', 'row', 'col')

    def __init__(self, row, col, panel=None):
        self.r = self.g = self.b = 0
        self.row = row
        self.col = col
        self.panel = panel

    # h,s,b are from 0 to 1
    def sethue(self, hue, brightness, saturation) :
        angle = hue*6%6.0
        brightness = min(max(float(brightness), 0.0), 1.0)
        saturation = min(max(float(saturation), 0.0), 1.0)
        r, g, b = 0, 0, 0
        if angle<2.0 :
            r=1
            if angle<1.0 :
                g = 0
                b = 1.0-angle
            else :
                g = angle-1.0
                b = 0
        if angle>=2.0 and angle<4.0 :
            g=1
            if angle<3.0 :
                r=3.0-angle
                b=0
            else :
                r=0
                b=angle-3.0
        if angle>=4.0 :
            b=1
            if angle<5.0 :
                g=5.0-angle
                r=0
            else :
                g=0
                r=angle-5.0
        self.r=brightness*(min(max(brightness-saturation, 0.0), 1.0)*r+saturation)
        self.g=brightness*(min(max(brightness-saturation, 0.0), 1.0)*g+saturation)
        self.b=brightness*(min(max(brightness-saturation, 0.0), 1.0)*b+saturation)

    def setrgb(self, red, green, blue):
        self.r = red
        self.g = green
        self.b = blue

    def __repr__(self):
        return '<RGBPixel: (%r, %r, %r)>' % (self.r, self.g, self.b)

class PanelIter(object):

    @numpycheck
    def blank_matrix(self):
        A = numpy.ndarray((self.height, self.width, 3), dtype=numpy.single)
        A[:] = 0
        return A

    @numpycheck
    def sethue(self, arr):
        for row in self.lights:
            for pixel in row:
                pixel.sethue(*arr[pixel.row, pixel.col])

    @numpycheck
    def setrgb(self, arr):
        for row in self.lights:
            for pixel in row:
                pixel.setrgb(*arr[pixel.row, pixel.col])

class LightPanel(PanelIter):
    changed = True
    def __init__(self, dmx, comp) :
        self.lights = [[RGBLight(j, i, self) for i in range(0,12)]
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
        self.changed = False

    def outputAndWait(self, fps) :
        self.output()
        endtime = time.time()-self.time
        if(1.0/fps > endtime) :
            time.sleep(1.0/fps-endtime)
        self.time = time.time()

class HalfLightPanel(PanelIter):
    changed = True
    # direction: 0 is "bottom right corner is (0,0)" and 1 is "bottom left ..."
    def __init__(self, dmx, direction) :
        self.outputdata = array.array('B', (0,) * 657)
        self.width = 6
        self.height = 12
        self.direction = direction
        self.lights = [[RGBLight(j, i, self) for i in range(0, self.width)]
                       for j in range(0, self.height)]
        self.dmx = dmx
        self.time = time.time()

    def output(self, wait_fps = None) :
        row = 0
        col = 0
        ptr = 1
        output = self.outputdata
        for i in range(0, 72) :
            row = i % 12
            if self.direction == 0 :
                col = 5-(i//12)
            else :
                col = i//12
            l = self.lights[row][col]
            output[ptr] = int(255*min(max(l.r ** 0.9, 0.0), 1.0))
            output[ptr + 1] = int(255*min(max(l.g ** 0.9, 0.0), 1.0))
            output[ptr + 2] = int(255*min(max(l.b ** 0.9, 0.0), 1.0))
            ptr += 3
        output[-1] = 191
        #if wait_fps:
        #    self._wait(wait_fps)
        self.dmx.send_dmx(output.tostring())
        self.changed = False

    def _wait(self, fps):
        curtime = time.time()
        endtime = curtime - self.time
        if 1.0 / fps > endtime:
            time.sleep(1.0 / fps - endtime)
        self.time = time.time()

    def outputAndWait(self, fps) :
        self.output()
        self._wait(fps)

class PanelComposite(PanelIter):
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
        for row in self.lights:
            for light in row:
                newlights[light.row][light.col] = light
        for row in panel.lights :
            for light in row :
                light.row = llrow + light.row
                light.col = llcol + light.col
                newlights[light.row][light.col] = light
        self.lights = newlights
    def output(self) :
        for panel in self.panels:
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
    for i in range(1,31) :
        ip, x, y = _get_panel_info(i)
        num = ((i - 1) & 15) + 1
        panel_part = HalfLightPanel(sPDS480caConnection(ip, num), 1-(i%2))
        panel.addPanel(panel_part, y, x)
    return panel

def _get_panel_info(i):
    ips = {0: '18.224.0.194',
           1: '18.224.0.238',}
    ip = ips[i // 17]
    x, y = 6 * ((i - 1) % 10), 12 * ((30 - i) // 10)
    return ip, x, y


if __name__=="__main__" :
    a = getDefaultPanel()
    color = 1
    import sys
    while True:

        for row in a.lights:
            for light in row:
                light.setrgb(255, 0, 0)
                a.outputAndWait(30)
        #sys.exit()
        for row in a.lights :
            for light in row :
                light.g=color
                a.outputAndWait(30)
        for row in a.lights :
            for light in row :
                light.b=color
                a.outputAndWait(30)
        color = 1.0-color
