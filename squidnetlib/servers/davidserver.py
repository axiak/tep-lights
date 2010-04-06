import os
from squidnet import sexp, squidprotocol as sp, squidserver as ss, dmx

sr = ss.ShellRunner()
lights = dmx.SimpleLights(dmx.DmxConnection("18.224.0.173", 6038, 0))


def quadsurf2(args):
    prog = '/home/david/gorlack-code-computer/quadsurf-new2/graph'
    print prog, args['brightness']
    sr.spawn(prog, [prog, args['brightness']])

serv = sp.SquidServer("davidxen", "david-xen.mit.edu", 2222, "David's computer")
d1 = sp.SquidDevice("eyeofgorlack", "The Eye of Gorlack")
serv.add_device(d1)
d1.add_message(sp.SquidMessage("quadsurf2",
                               "Run quadsurf-new2",
                               [sp.SquidArgument("brightness", sp.SquidRangeType())],
                               quadsurf2))

ss.run_server(serv)
