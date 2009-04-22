import dmx
import threading
import time

class Widget (threading.Thread) :
    def setPanel(self, panel) :
        self.panel = panel
    
    def init(self, panel) :
        # right before running.  override this
        pass

    def draw(self, panel) :
        # draw to panel and output in here.  override this
        pass

    def run(self) :
        self.running = True
        self.init(self.panel)
        while self.running :
            self.draw(self.panel)

class WidgetServer :
    def __init__(self, panel=dmx.getDefaultPanel()) :
        self.panel = panel
        self.running = False

    def run(self, widgetClasses) :
        self.running = True
        while self.running :
            for wc in widgetClasses :
                self.widget = wc()
                try :
                    self.widget.setPanel(self.panel)
                    self.widget.start()
                    #time.sleep(20)
                    raw_input("press enter for next widget")
                finally : # so we can ^C the thread
                    self.widget.running = False
