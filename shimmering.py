import dmxwidget
import math

class Shimmering (dmxwidget.Widget) :
    width = 1.0
    hue = 0.0
    shimmer_angle = 0.0
    center_x=0.0
    center_y=0.0
    dx=0.001
    dy=0.001
    def draw(self, panel) :
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
        for row in panel.lights:
            for pixel in row:
                self.setColor(panel, self.shimmer_angle, self.hue,
                              (float(pixel.col)/panel.width-0.5)*self.width*2-self.center_x,
                              (float(pixel.row)/panel.height-0.5)*self.width*2-self.center_y,
                              pixel.row, pixel.col)
        panel.outputAndWait(30)


    def setColor(self, panel, shimmer_angle, hue, x, y, lightrow, lightcol) :
        dist = math.cos(shimmer_angle/10)*x*y+math.cos(shimmer_angle)*x*x+math.sin(shimmer_angle)*y*y
        panel.lights[lightrow][lightcol].sethue(hue+dist/2.5, 1, 0)


if __name__=="__main__" :
    ws = dmxwidget.WidgetServer()
    ws.run([Shimmering])
