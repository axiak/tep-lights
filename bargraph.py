import dmx
import math
import random

panel = dmx.getDefaultPanel()
background = (0, 0, 0)
foreground = (0.5, 1, 0)
edge = (0.2, 1, 0)

def drawCol(panel, columns, top):
    for row in xrange(panel.height):
        for col in columns:
            if row > top:
                panel.lights[row][col].sethue(background[0], background[1], background[2])
            elif row == top:
                panel.lights[row][col].sethue(edge[0], edge[1], edge[2])
            else:
                panel.lights[row][col].sethue(foreground[0], foreground[1], foreground[2])
        

def run(panel, numcols):
    percol = int(panel.width / numcols)
    columns = [[] for i in xrange(numcols)]
    count = 0
    print numcols, percol
    for col in xrange(panel.width):
        print col, count, col-count/percol
        columns[(col-count)/percol].append(col)
        count = (count + 1) % percol
    print columns
    # main loop
    while True:
        heights = getheights()
        for col in xrange(numcols):
            drawCol(panel, columns[col], heights[col])
        panel.outputAndWait(30)

def getheights():
    return [random.randint(0, panel.height-1) for i in xrange(numcols)]

if __name__ == "__main__":
    numcols = panel.width/4
    print numcols, 
    run(panel, numcols)
