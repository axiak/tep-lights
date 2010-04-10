import dmxwidget
import math

class ColorTest (dmxwidget.Widget) :
    def init(self, panel) :
        self.t = 0
        self.goup = True
    def draw(self, panel) :
        for row in range(0, panel.height) :
            for col in range(0, panel.width) :
                panel.lights[row][col].sethue(col/float(panel.width), self.t/255.0, row/float(panel.height))
        panel.outputAndWait(30)
        if self.t < 255 and self.goup :
            self.t += 1
        elif self.goup and self.t==255 :
            self.goup = False
            self.t -= 1
        elif self.t > 0 :
            self.t -= 1
        else :
            self.goup = True
            self.t += 1

if __name__=="__main__" :
    dmxwidget.WidgetServer().run([ColorTest])
