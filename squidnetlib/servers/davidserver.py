import os
from squidnet import sexp, squidprotocol as sp, squidserver as ss, dmx

sr = ss.ShellRunner()

def quadsurf2(args):
    prog = '/home/david/gorlack-code-computer/quadsurf-new2/graph'
    sr.spawn(prog, [prog, args['brightness'].value])

serv = sp.SquidServer("david-xen", "david-xen.mit.edu", 2222, "David's computer")
d1 = sp.SquidDevice("eye-of-gorlack", "The Eye of Gorlack")
serv.add_device(d1)
d1.add_message(sp.SquidMessage("quadsurf2",
                               "Run quadsurf-new2",
                               [sp.SquidArgument("brightness",
                                                 sp.SquidRangeValue,
                                                 sp.SquidRangeValue(0.8))],
                               quadsurf2))

ss.run_server(serv)
