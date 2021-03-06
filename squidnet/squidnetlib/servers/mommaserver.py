#!/usr/bin/env python
import os
import pydaemon
from squidnet import sexp, squidprotocol as sp, squidserver as ss, dmx

DAEMON = True

if DAEMON:
    pydaemon.createDaemon()

speak_sr = ss.ShellRunner()
def handle_say(args) :
    words = args["text"].value
    print "Saying",words
    speak_sr.spawn("/usr/bin/say", ["say", words])

serv = sp.SquidServer("momma", "momma.mit.edu", 2222, "Study room computer")

d3 = sp.SquidDevice("computer", "The study room computer")
serv.add_device(d3)
d3.add_message(sp.SquidMessage("say",
                               "Says a phrase",
                               [sp.SquidArgument("text", sp.SquidStringValue)],
                               handle_say))

ss.run_server(serv, daemon=DAEMON)
