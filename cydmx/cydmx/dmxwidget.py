import threading
import time

#try:
#    import pyximport; pyximport.install(pyimport = False)
#except ImportError:
#    pass

import dmx


class Widget(threading.Thread) :
    _framecount = 0
    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        self.setDaemon(True)

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
        self._framecount = 0
        self._last_tick = 0
        self.init(self.panel)
        while self.running:
            if not self._framecount % 30:
                tick = time.time()
                if self._last_tick:
                    print "FPS: %0.2f" % (30 / (tick - self._last_tick))
                self._last_tick = tick
            self._framecount += 1

            self.draw(self.panel)

class WidgetServer :
    def __init__(self, panel=dmx.getDefaultPanel()) :
        self.panel = panel
        self.running = False

    def run(self, widgetClasses, cycle=None) :
        self.running = True
        while self.running :
            for wc in widgetClasses :
                self.widget = wc()
                try :
                    self.widget.setPanel(self.panel)
                    self.widget.start()
                    #time.sleep(20)
                    if not cycle:
                        raw_input("press enter for next widget")
                    else:
                        time.sleep(cycle)
                finally : # so we can ^C the thread
                    self.widget.running = False
