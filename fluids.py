import dmxwidget
import math
import random

class Fluids (dmxwidget.Widget) :
    def init(self, panel) :
        self.theta = 0.0
    def f(self, x, y, theta) :
        return math.cos(10*x*x*math.cos(0.1*theta) + 10*y*y*math.sin(0.1*theta)+math.cos(0.011*theta)*x*y)
    def draw(self, panel) :
        sunx = 1
        suny = 1
        sunz = 0
        sunlength = math.sqrt(sunx**2 + suny**2+sunz**2)
        sunx /= sunlength
        suny /= sunlength
        sunz /= sunlength
        self.theta += 0.1
        h = 2.0/panel.height
        for r in range(0, panel.height) :
            for c in range(0, panel.width) :
                x = (2.0*c-panel.width)/panel.width
                y = (2.0*r-panel.width)/panel.width
                dx = (self.f(x+h,y,self.theta)-self.f(x,y,self.theta))/h
                dy = (self.f(x,y+h,self.theta)-self.f(x,y,self.theta))/h
                intens = (-dx*sunx - dy*suny + sunz)/math.sqrt(1 + dx*dx + dy*dy)
                intens = (1+intens)/2
                panel.lights[r][c].sethue(0.8, intens, max(0.0,4.0*intens-3.0))
        panel.outputAndWait(30)

if __name__=="__main__" :
    ws = dmxwidget.WidgetServer()
    ws.run([Fluids])
