#!/usr/bin/python
import dmxwidget
from gol import GameOfLife
from shimmering import Shimmering
from surfball import SurfBall
from flames2 import Flames2

if __name__ == '__main__':
    ws = dmxwidget.WidgetServer()
    ws.run([GameOfLife, Shimmering, SurfBall, Flames2], cycle=120)
