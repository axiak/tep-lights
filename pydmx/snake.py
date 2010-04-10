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
obstruction = set()
obstruction.add((0,0))

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
    for loc in obstruction :
        panel.lights[(loc[0]+3*panel.height/2-centerrow)%panel.height][(loc[1]+3*panel.width/2-centercol)%panel.width].setrgb(0.5, 0.5, 0.5)
    panel.outputAndWait(6)

def move_forward() :
    global alive
    global snake
    global direct
    global food
    global panel
    global obstruction
    if alive :
        head=snake[-1]
        new_head = ((head[0]+direct[0])%panel.height,(head[1]+direct[1])%panel.width)
        
        for part in snake :
            if new_head[0] == part[0] and new_head[1] == part[1] :
                alive = False
        for ob in obstruction :
            if new_head[0] == ob[0] and new_head[1] == ob[1] :
                alive = False
        for f in food :
            if f[0] == new_head[0] and f[1] == new_head[1] :
                snake.append(head)
                snake.append(head)
                food.remove(f)
        if len(snake)>0 :
            snake.pop(0)
        if alive :
            snake.append(new_head)
    else :
        if len(snake)==0 :
            r = (random.randrange(panel.height), random.randrange(panel.width))
            snake = [r, r, r]
            direct=(0, 1)
            alive=True
        else :
            snake.pop(0)

    if random.random() < 0.07 :
        food.append((random.randrange(panel.height),random.randrange(panel.width)))
    if random.random() < 0.06 :
        l = len(obstruction)
        while l == len(obstruction) :
            i = random.randrange(l)
            testob = None
            for ob in obstruction :
                if i == 0 :
                    testob = ob
                    break
                i -= 1
            obstruction.add((random.randrange(-1,2)+testob[0], random.randrange(-1,2)+testob[1]))

try :
    while True :
        c = stdscr.getch()
        if c==ord('q') :
            break
        chdir = False
        if c==curses.KEY_UP :
            chdir = True
            newdirect = (1,0)
        if c==curses.KEY_DOWN :
            chdir = True
            newdirect = (-1,0)
        if c==curses.KEY_LEFT :
            chdir = True
            newdirect = (0,-1)
        if c==curses.KEY_RIGHT :
            chdir = True
            newdirect = (0,1)
        if chdir :
            if 10*newdirect[0]+newdirect[1] != -(10*direct[0]+direct[1]) :
                direct = newdirect
        disp_board()
        move_forward()
finally :
    curses.endwin()
