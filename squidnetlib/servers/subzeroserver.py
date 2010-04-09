#!/usr/bin/env python
import os
from squidnet import sexp, squidprotocol as sp, squidserver as ss, dmx

wall_visualizations = {
    'Shimmering': '/home/axiak/pydmx3/shimmering.py',
    'Surf Ball': '/home/axiak/pydmx3/surfball.py',
    'Flames': '/home/axiak/pydmx3/flames2.py',
    'Conway\'s Game of Life': '/home/axiak/pydmx3/gol.py',
}

wall_sr = ss.ShellRunner()

def handle_wall_color(args):
    prog = '/home/axiak/pydmx3/setcolor.py'
    arg = [str(c / 255.0) for c in args['color'].value]
    arg.insert(0, prog)
    wall_sr.spawn(prog, arg)
    print prog, arg

def handle_wall_viz(args):
    prog = wall_visualizations[args['visualization'].value]
    wall_sr.spawn(prog)


serv = sp.SquidServer("subzero", "subzero.mit.edu", 2222, "Subzero")

d1 = sp.SquidDevice("dining-room-wall", "Dining room wall!")
serv.add_device(d1)
 
d1.add_message(sp.SquidMessage("set",
                               "Set solid color",
                               [sp.SquidArgument("color", sp.SquidColorValue)],
                               handle_wall_color))

d1.add_message(sp.SquidMessage("visualization",
                               "Start a visualization",
                               [sp.SquidArgument("visualization", sp.SquidEnumFactory(*wall_visualizations))],
                               handle_wall_viz))


ss.run_server(serv)
