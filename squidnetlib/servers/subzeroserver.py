#!/usr/bin/env python
import os
from squidnet import sexp, squidprotocol as sp, squidserver as ss, dmx

wall_visualizations = {
    'Shimmering': 'shimmering',
    'Surf Ball': 'surfball',
    'Flames': 'flames2',
    'Conway\'s Game of Life': 'gol',
}

wall_sr = ss.ShellRunner()

def handle_wall_color(args):
    prog = '/home/axiak/pydmx5/setcolor.py'
    arg = [str(c / 255.0) for c in args['color'].value]
    arg.insert(0, prog)
    wall_sr.spawn(prog, arg)
    print prog, arg

def handle_wall_viz(args):
    #prog = '/home/axiak/pydmx5/run_module.py'
    viz = wall_visualizations[args['visualization'].value]
    prog = '/home/axiak/pydmx5/%s.py' % viz
    wall_sr.spawn(prog)

def handle_wall_image(args):
    prog = '/home/axiak/pydmx5/setimage.py'
    wall_sr.spawn(prog, [prog, args['Scaling'].value, args['image'].value])


serv = sp.SquidServer("subzero", "s0.mit.edu", 2222, "Subzero")

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


d1.add_message(sp.SquidMessage("image",
                               "Send an image",
                               [sp.SquidArgument("Scaling", sp.SquidEnumFactory('resize', 'thumbnail')),
                                sp.SquidArgument("image",
                                                 sp.SquidBase64FileValue)],
                               handle_wall_image))

ss.run_server(serv)
