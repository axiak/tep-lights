#!/usr/bin/env python
import os
from squidnet import sexp, squidprotocol as sp, squidserver as ss, dmx
import pygame
import random
from pygame.locals import *
import cStringIO as StringIO

say_sr = ss.ShellRunner()
def handle_say(args) :
    say_sr.spawn("/usr/bin/zenity", ['/usr/bin/zenity','--info','--text=%s %s' % (args['text'].value, args['awesomeness'].value)])

def handle_image(args):
    bitmap = pygame.image.load(StringIO.StringIO(args['image'].value.decode('base64')))
    bitmap = bitmap.convert()
    screen.blit(bitmap, (random.randint(0, 1024 - 400),
                         random.randint(0, 768 - 300)))
    pygame.display.flip()

serv = sp.SquidServer("zetazero", "zetazero.mit.edu", 2222, "Mike's computer")
d1 = sp.SquidDevice("computer", "Zetazero computer")
serv.add_device(d1)
d1.add_message(sp.SquidMessage("type",
                               "Type information to the screen", [sp.SquidArgument("text", sp.SquidStringType()),
sp.SquidArgument("awesomeness", sp.SquidRangeType(), sp.SquidValue(sp.SquidRangeType(), 0.5))],
                               handle_say))

d1.add_message(sp.SquidMessage("show",
                               "Show an image to one of the screens",
                               [sp.SquidArgument("image", sp.SquidBase64FileType())],
                               handle_image))

pygame.init()
screen = pygame.display.set_mode((1024, 768), HWSURFACE|DOUBLEBUF)
#pygame.display.toggle_fullscreen()


ss.run_server(serv)
