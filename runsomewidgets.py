import dmxwidget

from ball import Ball
from surfball import SurfBall
from clear import Clear
from clock import Clock
from colortest import ColorTest
from flames import Flames
from gol import GameOfLife
from shimmering import Shimmering

dmxwidget.WidgetServer().run([Ball, Clock, ColorTest, Flames, GameOfLife, Shimmering, SurfBall])
