import Tkinter
from dmx import *

class SimPanel:
    def __init__(self, width=24, height=24, gridsize=20):
        self.width = width
        self.height = height
        self.gridsize = float(gridsize)
        self.screen = Tkinter.Tk()
        self.screen.wm_title('Light Panel Simulator')
        self.background = Tkinter.Canvas(self.screen,
                                         width=self.gridsize*self.width,
                                         height=self.gridsize*self.height)
        self.background.pack()
        self.background['background'] = 'black'
        self.lights = [[RGBLight(j,i) for i in range(self.height)]
                       for j in range(self.width)]
        self.points = []
        for i in range(self.height):
            self.points.append([])
            for j in range(self.width):
                x = j*self.gridsize + self.gridsize/2
                y = i*self.gridsize + self.gridsize/2
                self.points[i].append(self.background.create_oval((x,y,x,y)))
        self.time = time.time()

    def output(self):
        for i in range(self.height):
            for j in range(self.width):
                x = j*self.gridsize + self.gridsize/2
                y = (self.height - i - 1)*self.gridsize + self.gridsize/2
                color = '#%02x%02x%02x' % (255*self.lights[i][j].r,
                                           255*self.lights[i][j].g,
                                           255*self.lights[i][j].b)
                #diameter = 3 + 3*max(self.lights[i][j].r, self.lights[i][j].g, self.lights[i][j].b)
                #self.background.coords(self.points[j][i], (x,y,x+diameter,y+diameter))
                self.background.coords(self.points[j][i], (x,y,x+5,y+5))
                self.background.itemconfig(self.points[j][i], fill=color)

    def outputAndWait(self, fps):
        self.output()
        endtime = time.time()-self.time
        if 1.0/fps > endtime:
            time.sleep(1.0/fps-endtime)
        self.time = time.time()
