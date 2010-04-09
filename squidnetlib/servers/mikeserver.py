#!/usr/bin/env python
import os
from squidnet import sexp, squidprotocol as sp, squidserver as ss, dmx
import pygame
import random
import threading
import time
from pygame.locals import *
import cStringIO as StringIO

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

say_sr = ss.ShellRunner()
def handle_type(args) :
    say_sr.spawn("/usr/bin/zenity", ['/usr/bin/zenity','--info','--text=%s %s' % (args['text'].value, args['awesomeness'].value)])

def handle_image(args):
    bitmap = pygame.image.load(StringIO.StringIO(args['image'].value.decode('base64')))
    bitmap = bitmap.convert()
    screen.blit(bitmap, (random.randint(0, 1024 - 400),
                         random.randint(0, 768 - 300)))
    pygame.display.flip()

speak_sr = ss.ShellRunner()
def handle_say(args) :
    words = args["text"].value
    speak_sr.spawn("/usr/bin/espeak", ["espeak", words])

serv = sp.SquidServer("zetazero", "zetazero.mit.edu", 2222, "Mike's computer")
d1 = sp.SquidDevice("computer", "Zetazero computer")
serv.add_device(d1)

d1.add_message(sp.SquidMessage("type",
                               "Type information to the screen",
                               [sp.SquidArgument("text", sp.SquidStringValue),
                                sp.SquidArgument("awesomeness",
                                                 sp.SquidEnumFactory("one",
                                                                     "two",
                                                                     "three",
                                                                     "four"),
                                                 "two")],
                               handle_type))

d1.add_message(sp.SquidMessage("show",
                               "Show an image to one of the screens",
                               [sp.SquidArgument("image",
                                                 sp.SquidBase64FileValue)],
                               handle_image))

d1.add_message(sp.SquidMessage("say",
                               "Says a phrase",
                               [sp.SquidArgument("text", sp.SquidStringValue)],
                               handle_say))

d2 = sp.SquidDevice("dining-room-wall", "Dining room wall!")
serv.add_device(d2)

d2.add_message(sp.SquidMessage("set",
                               "Set solid color",
                               [sp.SquidArgument("color", sp.SquidColorValue)],
                               handle_wall_color))

d2.add_message(sp.SquidMessage("visualization",
                               "Start a visualization",
                               [sp.SquidArgument("visualization", sp.SquidEnumFactory(*wall_visualizations))],
                               handle_wall_viz))

pygame.init()
screen = pygame.display.set_mode((1024, 768), HWSURFACE|DOUBLEBUF)

def threader():
    while True:
        pygame.display.flip()
        time.sleep(15)
t = threading.Thread(target=threader)
t.setDaemon(True)
t.start()


ss.run_server(serv)
