#!/usr/bin/python
from cydmx import dmx
import curses




stdscr = curses.initscr()
stdscr.keypad(1)
stdscr.nodelay(1)

panel = dmx.getDefaultPanel()

table = [[0 for row in range(panel.height)] for col in range(panel.width)]

bluePos = (0, 0, 3)
redPos = (panel.width - 1, panel.height - 1, 1)


blueDead = False
redDead = False

def disp_board():
    global panel
    global blueDead
    global redDead
    global table
    clearBoard(panel)
    if(blueDead and redDead):
        for row in panel.lights:
            for pixel in row:
                pixel.r = 1
                pixel.b = 1
    if(blueDead):
        for row in panel.lights:
            for pixel in row:
                pixel.r = 1
    elif(redDead):
        for row in panel.lights:
            for pixel in row:
                pixel.b = 1
    else:
    
    
        for i in xrange(len(table)):
            for j in xrange(len(table[i])):
                if(table[i][j] == 1):
                    panel.lights[j][i].b = 1
                elif(table[i][j] == 2):
                    panel.lights[j][i].r = 1
    panel.outputAndWait(6)



def clearBoard(panel):
    for row in panel.lights:
        for pixel in row:
            pixel.r = 0
            pixel.g = 0
            pixel.b = 0


def updateGame():
    global panel
    global bluePos
    global redPos
    global blueDead
    global redDead
    #manage blue snake
    bx, by, btheta = bluePos
    table[bx][by] = 1
    if(btheta == 0):
        bx+=1
    elif(btheta == 1):
        by+=1
    elif(btheta == 2):
        bx-=1
    elif(btheta == 3):
        by-=1
    
    if(bx < 0):
        bx = panel.width-1
    if(bx > panel.width - 1):
        bx = 0
    if(by < 0):
        by = panel.height - 1
    if(by > panel.height - 1):
        by = 0


    

    #manage the red snake
    rx, ry, rtheta = redPos
    table[rx][ry] = 2
    if(rtheta == 0):
        rx+=1
    elif(rtheta == 1):
        ry+=1
    elif(rtheta == 2):
        rx-=1
    elif(rtheta == 3):
        ry-=1

    if(rx < 0):
        rx = panel.width - 1
    if(rx > panel.width - 1):
        rx = 0
    if(ry < 0):
        ry = panel.height - 1
    if(ry > panel.height - 1):
        ry = 0
    bluePos = (bx, by, btheta)   
    redPos = (rx, ry, rtheta)
        
def testCollisions():
    #test collisions
    global bluePos
    global redPos
    global redDead
    global blueDead
    (rx, ry, rtheta) = redPos
    (bx, by, btheta) = bluePos
    if(rx == bx and ry == by):
        redDead = True
        blueDead = True
    if(table[rx][ry] == 1 or table[rx][ry] == 2):
        redDead = True
    if(table[bx][by] == 1 or table[bx][by] == 2):
        blueDead = True


try:
   while True :
       (bx, by, btheta) = bluePos
       (rx, ry, rtheta) = redPos
       c = stdscr.getch()
       if c==ord('q'):
           clearBoard(panel)
           panel.output()
           break
       if c==curses.KEY_UP and rtheta != 3:
           rtheta = 1
       if c==curses.KEY_DOWN and rtheta != 1:
           rtheta = 3
       if c==curses.KEY_LEFT and rtheta != 0:
           rtheta = 2
       if c==curses.KEY_RIGHT and rtheta != 2:
           rtheta = 0

       redPos = (rx, ry, rtheta)

       if c==ord('w') and btheta != 3:
           btheta = 1
       if c==ord('s') and btheta != 1:
           btheta = 3
       if c==ord('a') and btheta != 0:
           btheta = 2
       if c==ord('d') and btheta != 2:
           btheta = 0
           
       bluePos = (bx, by, btheta)

       if c==ord('r') and (redDead or blueDead):
           clearBoard(panel)
           for i in xrange(len(table)):
               for j in xrange(len(table[i])):
                   table[i][j] = 0
           redDead = False
           blueDead = False
           bluePos = (0, 0, 3)
           redPos = (panel.width - 1, panel.height - 1, 1)


       if not redDead and not blueDead:
           updateGame()
       disp_board()
       testCollisions()

       
finally :
    curses.endwin()
       

    
        
