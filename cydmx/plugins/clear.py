from cydmx import dmxwidget

class Clear (dmxwidget.Widget) :
    def draw(self, panel) :
        for row in panel.lights:
            for light in row:
                light.sethue(0, 0, 0)
        panel.outputAndWait(5)

if __name__=="__main__" :
    dmxwidget.WidgetServer().run([Clear])

