#!/usr/bin/env python
import os
from squidnet import sexp, squidprotocol as sp, squidserver as ss, dmx

say_sr = ss.ShellRunner()
def handle_say(args) :
    say_sr.spawn("/usr/bin/zenity", ['/usr/bin/zenity','--info','--text=%s' % args['text'].value])

def handle_awesome(args):
    say_sr.spawn("/usr/bin/zenity", ['/usr/bin/zenity','--info','--text=%s' % args['awesomeness'].value])

serv = sp.SquidServer("zetazero", "zetazero.mit.edu", 2222, "Mike's computer")
d1 = sp.SquidDevice("computer", "Zetazero computer")
serv.add_device(d1)
d1.add_message(sp.SquidMessage("type",
                               "Type information to the screen", [sp.SquidArgument("text", sp.SquidStringType())],
                               handle_say))

d1.add_message(sp.SquidMessage("awesome",
                               "Rate awesomeness", [sp.SquidArgument("awesomeness", sp.SquidRangeType(), sp.SquidValue(sp.SquidRangeType(), 0.5))],
                               handle_awesome))
ss.run_server(serv)
