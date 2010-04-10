import dmx
import math
import random
import stockquote
import time

def drawCol(panel, columns, top, fg=(0.4,1,0), bg=(0,0,0), edge=(0.2,0.6,0)):
    for row in xrange(panel.height):
        for col in columns:
            if row > top:
                panel.lights[row][col].sethue(bg[0], bg[1], bg[2])
            elif row == top:
                panel.lights[row][col].sethue(edge[0], edge[1], edge[2])
            else:
                panel.lights[row][col].sethue(fg[0], fg[1], fg[2])
        

def run(panel):
    global offset
    heights = getheights()
    numcols = len(heights)
    percol = int(panel.width / numcols)
    columns = [[] for i in xrange(numcols)]
    count = 0
    rest = []
    for col in xrange(panel.width):
        try:
            columns[int((col-count)/percol)].append(col)
        except:
            rest.append(col)
        count = (count + 1) % percol
    # main loop
    if numcols == panel.width:
        offset = (offset+0.4)%2
    else:
        offset = 0
    for col in xrange(numcols):
        drawCol(panel, columns[col], int(heights[col]), fg=(fore[0]*col+offset, fore[1], fore[2]))
    for col in rest:
        drawCol(panel, [col], 0, edge=(0, 0, 0))
    panel.output()

def getheights():
    heights.insert(0, (float(stockquote.get_quote("goog"))/25))
    if len(heights) > panel.width:
        heights.pop()
    return heights

if __name__ == "__main__":
    panel = dmx.getDefaultPanel()
    fore = [0.4, 1, 0]
    numcols = panel.width
    offset = 0
    heights = []
    while True:
        run(panel)
        time.sleep(300)
                       
