#!/usr/bin/python
import time
import math

from cydmx import dmxwidget

class Shimmering (dmxwidget.Widget) :
    width = 1.01
    hue = 0.0
    shimmer_angle = 0.0
    center_x=0.0
    center_y=0.0
    dx=0.001
    dy=0.001
    framecount = 0
    last_tick = 0
    array = None

    def _draw(self, panel) :
        import hotshot
        prof = hotshot.Profile("/tmp/shimmering-%03d.prof" % self.framecount)
        prof.runcall(self._draw, panel)


    def draw(self, panel):
        self.hue+=2/255.0;
        self.shimmer_angle += 0.05
        self.center_x+=self.dx*math.cos(self.shimmer_angle/100)
        self.center_y+=self.dy*math.sin(self.shimmer_angle/100)
        if self.center_x>self.width :
            self.dx = -self.dx
            self.center_x=1.0
        elif self.center_x < -1 :
            self.dx = -self.dx
            self.center_x=-1
        if self.center_y>1 :
            self.dy = -self.dy
            self.center_y=1
        elif self.center_y < -1 :
            self.dy=-self.dy
            self.center_y=-1

        shimmer_angle = self.shimmer_angle
        alpha, beta, gamma = math.cos(shimmer_angle / 10), math.cos(shimmer_angle), math.sin(shimmer_angle)
        width, center_x, center_y = self.width, self.center_x, self.center_y
        hue = self.hue
        pheight, pwidth = panel.height, panel.width
        for row in panel.lights:
            for pixel in row:
                cur_x = (float(pixel.col)/panel.width-0.5)*(width * 2)-center_x
                cur_y = (float(pixel.row)/panel.height-0.5)*(width * 2)-center_y
                dist = alpha * cur_x * cur_y \
                     + beta * cur_x**2 \
                     + gamma * cur_y**2

                pixel.sethue(hue + dist / 2.5, 1, 0)
        panel.outputAndWait(30)



if __name__=="__main__" :
    ws = dmxwidget.WidgetServer()
    ws.run([Shimmering])
