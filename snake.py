import dmx
import curses
import random

stdscr = curses.initscr()
stdscr.keypad(1)
stdscr.nodelay(1)

panel = dmx.getDefaultPanel()

snake = []
direct=(0,0)
food = []

alive = False

centerrow = 5
centercol = 5

def disp_board() :
    global panel
    global snake
    global centerrow
    global centercol
    if len(snake)>0 :
        centerrow = snake[-1][0]
        centercol = snake[-1][1]
    for row in panel.lights :
        for pixel in row :
            pixel.setrgb(0,0,0)
    for loc in snake :
        panel.lights[(loc[0]+3*panel.height/2-centerrow)%panel.height][(loc[1]+3*panel.width/2-centercol)%panel.width].r = 1.0
    for loc in food :
        panel.lights[(loc[0]+3*panel.height/2-centerrow)%panel.height][(loc[1]+3*panel.width/2-centercol)%panel.width].g = 1.0
    panel.outputAndWait(6)

def move_forward() :
    global alive
    global snake
    global direct
    global food
    global panel
    if alive :
        head=snake[-1]
        new_head = ((head[0]+direct[0])%panel.height,(head[1]+direct[1])%panel.width)
        
        for comp in snake :
            if new_head==comp :
                alive = False
                break
        for f in food :
            if f==new_head :
                snake.append(head)
                snake.append(head)
                food.remove(f)
        if len(snake)>0 :
            snake.pop(0)
        if alive :
            snake.append(new_head)
    else :
        if len(snake)==0 :
            snake = [(5,4),(5,5),(5,6)]
            direct=(0,1)
            alive=True
        else :
            snake.pop(0)

    if random.random() < 0.05 :
        food.append((random.randrange(panel.height),random.randrange(panel.width)))

try :
    while True :
        c = stdscr.getch()
        if c=='q' :
            break
        if c==curses.KEY_UP :
            direct = (1,0)
        if c==curses.KEY_DOWN :
            direct = (-1,0)
        if c==curses.KEY_LEFT :
            direct = (0,-1)
        if c==curses.KEY_RIGHT :
            direct = (0,1)
        disp_board()
        move_forward()
finally :
    curses.endwin()
