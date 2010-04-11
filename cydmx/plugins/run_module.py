try:
    import pyximport; pyximport.install()
except ImportError:
    pass
from cydmx import dmxwidget
import sys

def main():
    modname = sys.argv[1]
    module = __import__(modname.rsplit('.', 1)[0])
    widgets = []
    for name in dir(module):
        val = getattr(module, name)
        try:
            if issubclass(val, dmxwidget.Widget) and val != dmxwidget.Widget:
                widgets.append(val)
        except TypeError:
            pass
    ws = dmxwidget.WidgetServer()
    ws.run(widgets)
    
    


if __name__ == "__main__":
    main()
