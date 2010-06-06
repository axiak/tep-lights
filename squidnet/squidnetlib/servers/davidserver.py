#!/usr/bin/env python
import os
from squidnet import sexp, squidprotocol as sp, squidserver as ss, dmx

import pydaemon

pydaemon.createDaemon()

sr = ss.ShellRunner()

BASE_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'gorlack-code-computer')

programs = {
    'Quadsurf New 2': 'quadsurf-new2',
    'Quadsurf New 1': 'quadsurf-new1',
    'Hue Ball': 'hueball',
    'Quadsurf': 'quadsurf',
    'Blinky Cylon': 'blinkycylon',
    'Strange': 'strange',
    'Strobe Ball': 'strobeball',
    'Eye of Gorlack': 'wtf-1',
    'Paint Drip Up': 'paint-drip-up',
}

def viz(args):
    sr.kill()
    prog = os.path.join(BASE_DIR, programs[args['visualization'].value], 'graph')
    base = prog
    sr.spawn(prog, [base, str(args['brightness'].value)])

def setcolor(args):
    sr.kill()
    prog = os.path.join(BASE_DIR, 'setcolor', 'graph')
    color = [str(x / 256.0) for x in args['color'].value]
    color.insert(0, prog)
    sr.spawn(prog, color)

def setcolortemp(args):
    temp = 1800 + 7200 * args['temperature'].value
    import kwrgb
    kcon = kwrgb.kwrgb()
    bgColor = kcon.convertKRGB(3200, temp, False)
    sr.kill()
    prog = os.path.join(BASE_DIR, 'setcolor', 'graph')
    color = [str(x / 256.0) for x in bgColor]
    color.insert(0, prog)
    sr.spawn(prog, color)


serv = sp.SquidServer("david-xen", "david-xen.mit.edu", 2222, "David's computer")
d1 = sp.SquidDevice("eye-of-gorlack", "The Eye of Gorlack")
serv.add_device(d1)
d1.add_message(sp.SquidMessage("visualization",
                               "Run visualizations",
                               [
            sp.SquidArgument("visualization",
                             sp.SquidEnumFactory(*programs.keys())),
            sp.SquidArgument("brightness",
                             sp.SquidRangeValue,
                             0.8)],
                               viz))

d1.add_message(sp.SquidMessage("set",
                               'Set color',
                               [sp.SquidArgument("color",
                                                 sp.SquidColorValue, [230, 255, 179])],
                               setcolor))

d1.add_message(sp.SquidMessage("settemp",
                               'Set color temperature',
                               [sp.SquidArgument("temperature",
                                                 sp.SquidRangeValue,
                                                 0.2)],
                               setcolortemp))

ss.run_server(serv, daemon=True)
