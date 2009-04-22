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
        

def run(panel, numcols):
    heights = getheights(numcols)
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
    for col in xrange(numcols):
        drawCol(panel, columns[col], heights[col], fg=(fore[0]*col, fore[1], fore[2]))
    for col in rest:
        drawCol(panel, [col], 0, edge=(0, 0, 0))
    panel.output()

def getheights(numcols):
    #return [random.randint(0, panel.height-1) for i in xrange(numcols)]
    return heights

if __name__ == "__main__":
    panel = dmx.getDefaultPanel()
    fore = (0.4, 1, 0)
    companies = ["goog", "aapl", "msft", "ibm", "java", "sun"]
    numcols = len(companies)
    heights = []
    for col in xrange(len(companies)):
        heights.append(float(stockquote.get_quote(companies[col]))/25)
    run(panel, numcols)
