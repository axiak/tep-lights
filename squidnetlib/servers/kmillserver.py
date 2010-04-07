import os
from squidnet import sexp, squidprotocol as sp, squidserver as ss, dmx

sr = ss.ShellRunner()
lights = dmx.SimpleLights(dmx.DmxConnection("18.224.0.173", 6038, 0))

def handle_cycle(args) :
    sr.spawn("/Users/kyle/notes/projects/fft/chromatest")
def handle_stop(args) :
    sr.kill()
def handle_set(args) :
    sr.kill()
    color = args["color"]
    for i in range(0,26) :
        lights.lights[i][0].r = color.value[0]/255.0
        lights.lights[i][0].g = color.value[1]/255.0
        lights.lights[i][0].b = color.value[2]/255.0
    lights.output()

st_sr = ss.ShellRunner()
floor2 = dmx.SimpleLights(dmx.DmxConnection("18.224.1.156", 6038, 0))
floor3 = dmx.SimpleLights(dmx.DmxConnection("18.224.1.158", 6038, 0))
floor4 = dmx.SimpleLights(dmx.DmxConnection("18.224.1.159", 6038, 0))

def handle_st_cycle(args) :
    st_sr.spawn("/Users/kyle/notes/projects/fft/bigchromatest")
def handle_st_floor2(args) :
    color = args["color"]
    st_sr.kill()
    for i in range(0,5) :
        floor2.lights[i][0].r = color.value[0]/255.0
        floor2.lights[i][0].g = color.value[1]/255.0
        floor2.lights[i][0].b = color.value[2]/255.0
    floor2.output()
def handle_st_floor3(args) :
    color = args["color"]
    st_sr.kill()
    for i in range(0,5) :
        floor3.lights[i][0].r = color.value[0]/255.0
        floor3.lights[i][0].g = color.value[1]/255.0
        floor3.lights[i][0].b = color.value[2]/255.0
    floor3.output()
def handle_st_floor4(args) :
    color = args["color"]
    st_sr.kill()
    for i in range(0,5) :
        floor4.lights[i][0].r = color.value[0]/255.0
        floor4.lights[i][0].g = color.value[1]/255.0
        floor4.lights[i][0].b = color.value[2]/255.0
    floor4.output()
def handle_st_set(args) :
    handle_st_floor2(args)
    handle_st_floor3(args)
    handle_st_floor4(args)
def handle_st_stop(args) :
    st_sr.kill()

speak_sr = ss.ShellRunner()
def handle_say(args) :
    words = args["text"].value
    print "Saying",words
    speak_sr.spawn("/usr/bin/say", ["say", words])

serv = sp.SquidServer("kmill", "kmill.mit.edu", 2222, "Kyle's computer")
d1 = sp.SquidDevice("22-lights", "The lights in 22")
serv.add_device(d1)
d1.add_message(sp.SquidMessage("cycle",
                               "Cycle the lights", [],
                               handle_cycle))
d1.add_message(sp.SquidMessage("set",
                               "Set the color of the lights",
                               [sp.SquidArgument("color", sp.SquidColorValue)],
                               handle_set))
d1.add_message(sp.SquidMessage("stop",
                               "Stops the lights", [],
                               handle_stop))

d2 = sp.SquidDevice("stairwell", "The stairwell lights")
serv.add_device(d2)
d2.add_message(sp.SquidMessage("cycle",
                               "Cycle the lights", [],
                               handle_st_cycle))
d2.add_message(sp.SquidMessage("set-floor2",
                               "Set the color of the second landing",
                               [sp.SquidArgument("color", sp.SquidColorValue)],
                               handle_st_floor2))
d2.add_message(sp.SquidMessage("set-floor3",
                               "Set the color of the third landing",
                               [sp.SquidArgument("color", sp.SquidColorValue)],
                               handle_st_floor3))
d2.add_message(sp.SquidMessage("set-floor4",
                               "Set the color of the fourth landing",
                               [sp.SquidArgument("color", sp.SquidColorValue)],
                               handle_st_floor4))
d2.add_message(sp.SquidMessage("set",
                               "Set the color of the stairwell",
                               [sp.SquidArgument("color", sp.SquidColorValue)],
                               handle_st_set))
d2.add_message(sp.SquidMessage("stop",
                               "Stop the lights", [],
                               handle_st_stop))

d3 = sp.SquidDevice("computer", "Kyle's computer")
serv.add_device(d3)
d3.add_message(sp.SquidMessage("say",
                               "Says a phrase",
                               [sp.SquidArgument("text", sp.SquidStringValue)],
                               handle_say))

ss.run_server(serv)
