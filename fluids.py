import dmxwidget
import math
import random

class FluidsTest (dmxwidget.Widget) :
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

class Fluids (dmxwidget.Widget) :
    def init(self, panel) :
        self.heights = [[0.0 for col in row] for row in panel.lights]
        self.veloc = [[0.0 for col in row] for row in panel.lights]
        self.heights[5][5] = 2.0
        self.boardwidth = 2.0
        self.boardheight = 2.0
    def f(self, x, y, theta) :
        return math.cos(10*x*x*math.cos(0.1*theta) + 10*y*y*math.sin(0.1*theta)+math.cos(0.011*theta)*x*y)
    def updateFluid(self) :
        dampen=0.005 # higher is more
        c2 = 0.05
        dt = 0.05
        h = self.boardwidth/len(self.heights)
        height = len(self.veloc)
        width = len(self.veloc[0])
        if random.random() < 0.008 :
            amount = 4*random.random()-2.0
            locrow = random.randrange(0, height)
            loccol = random.randrange(0, width)
            self.heights[locrow][loccol] += amount
            self.veloc[locrow][loccol] += amount
        for row in xrange(height) :
            for col in xrange(width) :
                drow2 = (self.heights[(row+1)%height][col]-2*self.heights[row][col]+self.heights[(row-1)%height][col])/h**2
                dcol2 = (self.heights[row][(col+1)%width]-2*self.heights[row][col]+self.heights[row][(col-1)%width])/h**2
                df2 = c2 * (drow2+dcol2)
                self.veloc[row][col] += df2*dt - self.veloc[row][col]*dampen
        for row in xrange(height) :
            for col in xrange(width) :
                self.heights[row][col] += self.veloc[row][col] * dt
    def draw(self, panel) :
        sunx = 1
        suny = 1
        sunz = 0.5
        sunlength = math.sqrt(sunx**2 + suny**2+sunz**2)
        sunx /= sunlength
        suny /= sunlength
        sunz /= sunlength
        
        self.updateFluid()
        h = 2.0/self.boardwidth
        for r in range(0, panel.height) :
            for c in range(0, panel.width) :
                dx = (self.heights[r][(c+1)%panel.width]-self.heights[r][c])
                dy = (self.heights[(r+1)%panel.height][c]-self.heights[r][c])
                intens = (-dx*sunx - dy*suny + sunz)/math.sqrt(1 + dx*dx + dy*dy)
                intens = (1+intens)/2
                panel.lights[r][c].sethue(0.8, intens, max(0.0,4.0*intens-3.0))
        panel.outputAndWait(30)

if __name__=="__main__" :
    ws = dmxwidget.WidgetServer()
    ws.run([Fluids])
