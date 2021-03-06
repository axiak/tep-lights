#!/usr/bin/env python
import os
import shlex
from squidnet import sexp, squidprotocol as sp, squidserver as ss, dmx

DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

print DIR

wall_visualizations = {
    'Shimmering': 'cdmx/plugins/shimmering',
    'Electric Sheep': '/usr/bin/mplayer /home/axiak/electricsheep-sample.mov -loop 0',
    'Surf Ball': 'cydmx/plugins/surfball.py',
    'Flames 2': 'cydmx/plugins/flames2.py',
    'Conway\'s Game of Life': 'cydmx/plugins/gol.py',
    'Cycle between them': 'cydmx/plugins/cycle.py',
    'Flames': 'cydmx/plugins/flames.py',
    'Fluids': 'cydmx/plugins/fluids.py',
    'Circles': 'cdmx/plugins/geomtest',
    'Strobe': ['cdmx/plugins/shimmering', 'cdmx/plugins/strobe'],
}

wall_sr = ss.ShellRunner()

server_sr = ss.ShellRunner()
server_sr.spawn(os.path.join(DIR, 'cdmx', 'src', 'naserver'))


def handle_wall_color(args):
    prog = os.path.join(DIR, 'cydmx', 'plugins', 'setcolor.py')
    arg = [str(c / 255.0) for c in args['color'].value]
    arg.insert(0, prog)
    wall_sr.spawn(prog, arg)

def handle_extinguish(args):
    prog = os.path.join(DIR, 'cydmx', 'plugins', 'setcolor.py')
    wall_sr.spawn(prog, [prog, '0', '0', '0', '1'])

def handle_wall_viz(args):
    viz = wall_visualizations[args['visualization'].value]
    if isinstance(viz, basestring):
        viz = [viz]
    args = []
    for v in viz:
        if isinstance(v, basestring):
            v = os.path.join(DIR, v)
            v = shlex.split(v)
            args.append(v[0])
            args.append(v)
    wall_sr.spawn(*args)


def handle_wall_text(args):
    prog = os.path.join(DIR, 'cydmx', 'plugins', 'text.py')
    wall_sr.spawn(prog, [prog, args['text'].value,
                         str(args['color'].value[0]),
                         str(args['color'].value[1]),
                         str(args['color'].value[2]),
                         str(args['speed'].value)])


def handle_wall_image(args):
    prog = os.path.join(DIR, 'cydmx', 'plugins', 'setimage.py')
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

d1.add_message(sp.SquidMessage("text",
                               "Send text",
                               [sp.SquidArgument("text", sp.SquidStringValue),
                                sp.SquidArgument("color", sp.SquidColorValue),
                                sp.SquidArgument("speed", sp.SquidRangeValue,
                                                 0.5),],
                               handle_wall_text))

d1.add_message(sp.SquidMessage("extinguish",
                               "Turn everything off",
                               [],
                               handle_extinguish))

ss.run_server(serv)
