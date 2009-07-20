
def write(panel, text, cornerx=None, cornery=None, color=(0,1,0), size=(4,5), clear=True, show=False):
    hue, sat, lum = color
    if clear:
        for row in panel.lights:
            for pixel in row:
                pixel.sethue(0,0,0)
    if cornerx == None: cornerx = 0
    if cornery == None: cornery = panel.height - size[1]
    if size not in CHARS.keys():
        print 'ERROR: selected size not implemented'
        return cornerx, cornery
    chars = CHARS[size]
    lastkerning = ([0 for i in range(0, size[1])],[0 for i in range(0, size[1])])
    first = True # first in line? (i.e. bunk kerning data?)
    for char in text:
        if char==' ' :
            dist = (size[0]+1)/2+1
            lastkerning = ([0 for i in range(0, size[1])],[0 for i in range(0, size[1])])
        else :
            dist = max([lastkerning[1][i] - KERNING[size][char][0][i] for i in range(0, size[1])]) + 2
            lastkerning = KERNING[size][char]
        if not first :
            cornerx += dist
        first = False
        if (cornerx > panel.width-1
            or (char==' ' and cornerx + size[0] > panel.width-1)
            or (char != ' ' and WIDTH[size][char] + cornerx > panel.width-1)) :
            cornerx = 0
            cornery -= size[1] + 1 # the +1 is to leave a horizontal gap
        if cornery > panel.height-1:
            print 'Too much text for the screen!'
            break
        else:
            if char not in chars:
                print 'WARNING: character "%s" not implemented.' % char
                char = '-'
            for x,y in chars[char]:
                panel.lights[cornery+y][cornerx+x].sethue(hue, sat, lum)
            #print 'added char', char
    if show:
        panel.output()
    return cornerx, cornery

def scroll(panel, text, box=None, color=(0,1,0), size=(6,7), clear=True, repeat=True, fps=5):
    hue, sat, lum = color
    if clear:
        for row in panel.lights:
            for pixel in row:
                pixel.sethue(0,0,0)
    if box == None:
        box = (0, panel.width-1, panel.height-size[1]) # it's (xmin, xmax, ymin)
    if size not in CHARS.keys():
        print 'ERROR: selected size not implemented'
        return
    chars = CHARS[size]
    while True:
        for i in xrange(0, box[1]-box[0]+(size[0]*len(text))):
            for row in panel.lights[box[2]:box[2]+size[1]]:
                for pixel in row[box[0]:box[1]+1]:
                    pixel.sethue(0,0,0)
            cornerx = box[1] - i
            for char in text:
                if char not in chars:
                    print 'WARNING: character "%s" not implemented.' % char
                    char = '-'
                for x,y in chars[char]:
                    thisx = cornerx+x
                    if thisx >= box[0] and thisx <= box[1]:
                        panel.lights[box[2]+y][thisx].sethue(hue, sat, lum)
                cornerx += size[0]
                if cornerx > box[1]:
                    break
            panel.outputAndWait(fps)
        if not repeat:
            break

# use sys.argv !


CHARS_4_5 = {'A': [(0,0),(0,1),(0,2),(0,3),(1,2),(1,4),(2,2),(2,4),(3,0),(3,1),(3,2),(3,3)],
             'B': [(0,0),(0,1),(0,2),(0,3),(0,4),(1,0),(1,2),(1,4),(2,0),(2,2),(2,4),(3,1),(3,3)],
             'C': [(0,1),(0,2),(0,3),(1,0),(1,4),(2,0),(2,4),(3,1),(3,3)],
             'D': [(0,0),(0,1),(0,2),(0,3),(0,4),(1,0),(1,4),(2,0),(2,4),(3,1),(3,2),(3,3)],
             'E': [(0,0),(0,1),(0,2),(0,3),(0,4),(1,0),(1,2),(1,4),(2,0),(2,2),(2,4),(3,0),(3,4)],
             'F': [(0,0),(0,1),(0,2),(0,3),(0,4),(1,2),(1,4),(2,2),(2,4),(3,4)],
             'G': [(0,1),(0,2),(0,3),(1,0),(1,4),(2,0),(2,2),(2,4),(3,1),(3,2),(3,4)],
             'H': [(0,0),(0,1),(0,2),(0,3),(0,4),(1,2),(2,2),(3,0),(3,1),(3,2),(3,3),(3,4)],
             'I': [(1,0),(1,4),(2,0),(2,1),(2,2),(2,3),(2,4),(3,0),(3,4)],
             'J': [(0,1),(0,4),(1,0),(1,4),(2,1),(2,2),(2,3),(2,4),(3,4)],
             'K': [(0,0),(0,1),(0,2),(0,3),(0,4),(1,2),(2,1),(2,3),(3,0),(3,4)],
             'L': [(0,0),(0,1),(0,2),(0,3),(0,4),(1,0),(2,0),(3,0)],
             'M': [(0,0),(0,1),(0,2),(0,3),(0,4),(1,2),(1,3),(2,2),(2,3),(3,0),(3,1),(3,2),(3,3),(3,4)],
             'N': [(0,0),(0,1),(0,2),(0,3),(0,4),(1,2),(2,1),(3,0),(3,1),(3,2),(3,3),(3,4)],
             'O': [(0,1),(0,2),(0,3),(1,0),(1,4),(2,0),(2,4),(3,1),(3,2),(3,3)],
             'P': [(0,0),(0,1),(0,2),(0,3),(0,4),(1,2),(1,4),(2,2),(2,4),(3,3)],
             'Q': [(0,1),(0,2),(0,3),(1,0),(1,4),(2,0),(2,1),(2,4),(3,0),(3,1),(3,2),(3,3)],
             'R': [(0,0),(0,1),(0,2),(0,3),(0,4),(1,2),(1,4),(2,1),(2,2),(2,4),(3,0),(3,3)],
             'S': [(0,0),(0,3),(1,0),(1,2),(1,4),(2,0),(2,2),(2,4),(3,1),(3,4)],
             'T': [(0,4),(1,4),(2,0),(2,1),(2,2),(2,3),(2,4),(3,4)],
             'U': [(0,1),(0,2),(0,3),(0,4),(1,0),(2,0),(3,1),(3,2),(3,3),(3,4)],
             'V': [(0,2),(0,3),(0,4),(1,0),(1,1),(2,0),(2,1),(3,2),(3,3),(3,4)],
             'W': [(0,1),(0,2),(0,3),(0,4),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2),(3,1),(3,2),(3,3),(3,4)],
             'X': [(0,0),(0,1),(0,3),(0,4),(1,2),(2,2),(3,0),(3,1),(3,3),(3,4)],
             'Y': [(0,3),(0,4),(1,2),(2,0),(2,1),(2,2),(3,3),(3,4)],
             'Z': [(0,0),(0,1),(0,4),(1,0),(1,2),(1,4),(2,0),(2,3),(2,4),(3,0),(3,4)],
             '1': [(0,0),(1,0),(1,3),(2,0),(2,1),(2,2),(2,3),(2,4),(3,0)],
             '2': [(0,0),(0,3),(1,0),(1,1),(1,4),(2,0),(2,2),(2,4),(3,0),(3,2),(3,3)],
             '3': [(0,0),(0,4),(1,0),(1,2),(1,4),(2,0),(2,2),(2,4),(3,1),(3,3)],
             '4': [(0,2),(0,3),(0,4),(1,2),(2,0),(2,1),(2,2),(2,3),(2,4),(3,2)],
             '5': [(0,0),(0,2),(0,3),(0,4),(1,0),(1,2),(1,4),(2,0),(2,2),(2,4),(3,1),(3,4)],
             '6': [(0,1),(0,2),(0,3),(1,0),(1,2),(1,4),(2,0),(2,2),(2,4),(3,1),(3,4)],
             '7': [(0,4),(1,0),(1,4),(2,1),(2,2),(2,4),(3,3),(3,4)],
             '8': [(0,1),(0,3),(1,0),(1,2),(1,4),(2,0),(2,2),(2,4),(3,1),(3,3)],
             '9': [(0,3),(1,2),(1,4),(2,2),(2,4),(3,0),(3,1),(3,2),(3,3)],
             '0': [(0,1),(0,2),(0,3),(1,0),(1,1),(1,4),(2,0),(2,2),(2,4),(3,1),(3,2),(3,3)],
             '.': [(1,0)],
             ',': [(0,0),(1,1)],
             ':': [(1,1),(1,3)],
             '?': [(0,3),(1,4),(2,0),(2,2),(2,4),(3,2),(3,3)],
             '!': [(1,0),(1,2),(1,3),(1,4)],
             '-': [(0,2),(1,2),(2,2),(3,2)],
             "'": [(1,3),(1,4)],
             '/': [(0,1),(1,2),(2,3),(3,4)],
             ' ': []}

CHARS_6_7 = {'A': [(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),
                   (1,3),(1,6),
                   (2,3),(2,6),
                   (3,3),(3,6),
                   (4,0),(4,1),(4,2),(4,3),(4,4),(4,5)],
             'B': [(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),
                   (1,0),(1,3),(1,6),
                   (2,0),(2,3),(2,6),
                   (3,0),(3,3),(3,6),
                   (4,1),(4,2),(4,4),(4,5)],
             'C': [(0,1),(0,2),(0,3),(0,4),(0,5),
                   (1,0),(1,6),
                   (2,0),(2,6),
                   (3,0),(3,6),
                   (4,1),(4,5)],
             'D': [(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),
                   (1,0),(1,6),
                   (2,0),(2,6),
                   (3,0),(3,6),
                   (4,1),(4,2),(4,3),(4,4),(4,5)],
             'E': [(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),
                   (1,0),(1,3),(1,6),
                   (2,0),(2,3),(2,6),
                   (3,0),(3,3),(3,6),
                   (4,0),(4,6)],
             'F': [(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),
                   (1,3),(1,6),
                   (2,3),(2,6),
                   (3,3),(3,6),
                   (4,6)],
             'G': [(0,1),(0,2),(0,3),(0,4),(0,5),
                   (1,0),(1,6),
                   (2,0),(2,3),(2,6),
                   (3,0),(3,3),(3,6),
                   (4,0),(4,1),(4,2),(4,3),(4,5)],
             'H': [(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),
                   (1,3),
                   (2,3),
                   (3,3),
                   (4,0),(4,1),(4,2),(4,3),(4,4),(4,5),(4,6)],
             'I': [(1,0),(1,6),
                   (2,0),(2,1),(2,2),(2,3),(2,4),(2,5),(2,6),
                   (3,0),(3,6)],
             'J': [(0,1),
                   (1,0),
                   (2,0),(2,6),
                   (3,1),(3,2),(3,3),(3,4),(3,5),(3,6),
                   (4,6)],
             'K': [(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),
                   (1,3),
                   (2,2),(2,4),
                   (3,1),(3,5),
                   (4,0),(4,6)],
             'L': [(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),
                   (1,0),
                   (2,0),
                   (3,0),
                   (4,0)],
             'M': [(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),
                   (1,5),
                   (2,3),(2,4),
                   (3,5),
                   (4,0),(4,1),(4,2),(4,3),(4,4),(4,5),(4,6)],
             'N': [(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),
                   (1,4),
                   (2,3),
                   (3,2),
                   (4,0),(4,1),(4,2),(4,3),(4,4),(4,5),(4,6)],
             'O': [(0,1),(0,2),(0,3),(0,4),(0,5),
                   (1,0),(1,6),
                   (2,0),(2,6),
                   (3,0),(3,6),
                   (4,1),(4,2),(4,3),(4,4),(4,5)],
             'P': [(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),
                   (1,3),(1,6),
                   (2,3),(2,6),
                   (3,3),(3,6),
                   (4,4),(4,5)],
             'Q': [(0,1),(0,2),(0,3),(0,4),(0,5),
                   (1,0),(1,6),
                   (2,0),(2,2),(2,6),
                   (3,1),(3,6),
                   (4,0),(4,2),(4,3),(4,4),(4,5)],
             'R': [(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),
                   (1,3),(1,6),
                   (2,2),(2,3),(2,6),
                   (3,1),(3,3),(3,6),
                   (4,0),(4,4),(4,5)],
             'S': [(0,0),(0,4),(0,5),
                   (1,0),(1,3),(1,6),
                   (2,0),(2,3),(2,6),
                   (3,0),(3,3),(3,6),
                   (4,1),(4,2),(4,6)],
             'T': [(0,6),
                   (1,6),
                   (2,0),(2,1),(2,2),(2,3),(2,4),(2,5),(2,6),
                   (3,6),
                   (4,6)],
             'U': [(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),
                   (1,0),
                   (2,0),
                   (3,0),
                   (4,1),(4,2),(4,3),(4,4),(4,5),(4,6)],
             'V': [(0,3),(0,4),(0,5),(0,6),
                   (1,1),(1,2),
                   (2,0),
                   (3,1),(3,2),
                   (4,3),(4,4),(4,5),(4,6)],
             'W': [(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),
                   (1,0),
                   (2,1),(2,2),(2,3),
                   (3,0),
                   (4,1),(4,2),(4,3),(4,4),(4,5),(4,6)],
             'X': [(0,0),(0,1),(0,5),(0,6),
                   (1,2),(1,4),
                   (2,3),
                   (3,2),(3,4),
                   (4,0),(4,1),(4,5),(4,6)],
             'Y': [(0,4),(0,5),(0,6),
                   (1,3),
                   (2,0),(2,1),(2,2),
                   (3,3),
                   (4,4),(4,5),(4,6)],
             'Z': [(0,0),(0,1),(0,6),
                   (1,0),(1,2),(1,6),
                   (2,0),(2,3),(2,6),
                   (3,0),(3,4),(3,6),
                   (4,0),(4,5),(4,6)],
             'a': [(0,1),
                   (1,0),(1,2),(1,4),
                   (2,0),(2,2),(2,4),
                   (3,0),(3,2),(3,4),
                   (4,0),(4,1),(4,2),(4,3)],
             'b': [(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),
                   (1,0),(1,3),
                   (2,0),(2,4),
                   (3,0),(3,4),
                   (4,1)],
             'c': [(0,1),(0,2),(0,3),
                   (1,0),(1,4),
                   (2,0),(2,4),
                   (3,0),(3,4),
                   (4,1)],
             'd': [(0,1),(0,2),(0,3),
                   (1,0),(1,4),
                   (2,0),(2,4),
                   (3,0),(3,3),
                   (4,0),(4,1),(4,2),(4,3),(4,4),(4,5),(4,6)],
             'e': [(0,1),(0,2),(0,3),
                   (1,0),(1,2),(1,4),
                   (2,0),(2,2),(2,4),
                   (3,0),(3,2),(3,4),
                   (4,2),(4,3)],
             'f': [(0,3),
                   (1,0),(1,1),(1,2),(1,3),(1,4),(1,5),
                   (2,3),(2,6),
                   (3,6),
                   (4,5)],
             'g': [(0,3),(0,4),
                   (1,0),(1,2),(1,5),
                   (2,0),(2,2),(2,5),
                   (3,0),(3,2),(3,5),
                   (4,1),(4,2),(4,3),(4,4),(4,5)],
             'h': [(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),
                   (1,3),
                   (2,4),
                   (3,4),
                   (4,0),(4,1),(4,2),(4,3)],
             'i': [(1,0),(1,4),
                   (2,0),(2,1),(2,2),(2,3),(2,4),(2,6),
                   (3,0)],
             'j': [(0,1),
                   (1,0),
                   (2,0),(2,4),
                   (3,1),(3,2),(3,3),(3,4),(3,6)],
             'k': [(1,0),(1,1),(1,2),(1,3),(1,4),(1,5),(1,6),
                   (2,2),
                   (3,1),(3,3),
                   (4,0),(4,3)],
             'l': [(1,0),(1,6),
                   (2,0),(2,1),(2,2),(2,3),(2,4),(2,5),(2,6),
                   (3,0)],
             'm': [(0,0),(0,1),(0,2),(0,3),(0,4),
                   (1,4),
                   (2,2),(2,3),
                   (3,4),
                   (4,0),(4,1),(4,2),(4,3)],
             'n': [(0,0),(0,1),(0,2),(0,3),(0,4),
                   (1,3),
                   (2,4),
                   (3,4),
                   (4,0),(4,1),(4,2),(4,3)],
             'o': [(0,1),(0,2),(0,3),
                   (1,0),(1,4),
                   (2,0),(2,4),
                   (3,0),(3,4),
                   (4,1),(4,2),(4,3)],
             'p': [(0,0),(0,1),(0,2),(0,3),(0,4),
                   (1,2),(1,4),
                   (2,2),(2,4),
                   (3,2),(3,4),
                   (4,3)],
             'q': [(0,3),
                   (1,2),(1,4),
                   (2,2),(2,4),
                   (3,2),(3,3),
                   (4,0),(4,1),(4,2),(4,3),(4,4)],
             'r': [(0,0),(0,1),(0,2),(0,3),(0,4),
                   (1,3),
                   (2,4),
                   (3,4),
                   (4,3)],
             's': [(0,0),(0,3),
                   (1,0),(1,2),(1,4),
                   (2,0),(2,2),(2,4),
                   (3,0),(3,2),(3,4),
                   (4,1)],
             't': [(0,4),
                   (1,1),(1,2),(1,3),(1,4),(1,5),(1,6),
                   (2,0),(2,4),
                   (3,0),
                   (4,1)],
             'u': [(0,1),(0,2),(0,3),(0,4),
                   (1,0),
                   (2,0),
                   (3,1),
                   (4,0),(4,1),(4,2),(4,3),(4,4)],
             'v': [(0,2),(0,3),(0,4),
                   (1,1),
                   (2,0),
                   (3,1),
                   (4,2),(4,3),(4,4)],
             'w': [(0,1),(0,2),(0,3),(0,4),
                   (1,0),
                   (2,1),(2,2),
                   (3,0),
                   (4,1)],
             'x': [(0,0),(0,4),
                   (1,1),(1,3),
                   (2,2),
                   (3,1),(3,3),
                   (4,0),(4,4)],
             'y': [(0,3),(0,4),(0,5),
                   (1,0),(1,2),
                   (2,0),(2,2),
                   (3,0),(3,2),
                   (4,1),(4,2),(4,3),(4,4),(4,5)],
             'z': [(0,0),(0,4),
                   (1,0),(1,1),(1,4),
                   (2,0),(2,2),(2,4),
                   (3,0),(3,3),(3,4),
                   (4,0),(4,4)],
             '1': [(1,0),(1,5),
                   (2,0),(2,1),(2,2),(2,3),(2,4),(2,5),(2,6),
                   (3,0)],
             '2': [(0,0),(0,5),
                   (1,0),(1,1),(1,6),
                   (2,0),(2,2),(2,6),
                   (3,0),(3,3),(3,6),
                   (4,0),(4,4),(4,5)],
             '3': [(0,1),(0,6),
                   (1,0),(1,6),
                   (2,0),(2,4),(2,6),
                   (3,0),(3,3),(3,5),(3,6),
                   (4,1),(4,2),(4,6)],
             '4': [(0,2),(0,3),
                   (1,2),(1,4),
                   (2,2),(2,5),
                   (3,0),(3,1),(3,2),(3,3),(3,4),(3,5),(3,6),
                   (4,2)],
             '5': [(0,1),(0,4),(0,5),(0,6),
                   (1,0),(1,4),(1,6),
                   (2,0),(2,4),(2,6),
                   (3,0),(3,4),(3,6),
                   (4,1),(4,2),(4,3),(4,6)],
             '6': [(0,1),(0,2),(0,3),(0,4),
                   (1,0),(1,3),(1,5),
                   (2,0),(2,3),(2,6),
                   (3,0),(3,3),(3,6),
                   (4,1),(4,2)],
             '7': [(0,6),
                   (1,0),(1,1),(1,2),(1,6),
                   (2,3),(2,6),
                   (3,4),(3,6),
                   (4,5),(4,6)],
             '8': [(0,1),(0,2),(0,4),(0,5),
                   (1,0),(1,3),(1,6),
                   (2,0),(2,3),(2,6),
                   (3,0),(3,3),(3,6),
                   (4,1),(4,2),(4,4),(4,5)],
             '9': [(0,4),(0,5),
                   (1,0),(1,3),(1,6),
                   (2,0),(2,3),(2,6),
                   (3,1),(3,3),(3,6),
                   (4,2),(4,3),(4,4),(4,5)],
             '0': [(0,1),(0,2),(0,3),(0,4),(0,5),
                   (1,0),(1,2),(1,6),
                   (2,0),(2,3),(2,6),
                   (3,0),(3,4),(3,6),
                   (4,1),(4,2),(4,3),(4,4),(4,5)],
             '.': [(1,0),(1,1),(2,0),(2,1)],
             ',': [(1,0),(1,2),(2,1),(2,2)],
             ';': [(1,0),(1,2),(1,4),(1,5),
                   (2,1),(2,2),(2,4),(2,5)],
             ':': [(1,1),(1,2),(1,4),(1,5),
                   (2,1),(2,2),(2,4),(2,5)],
             '?': [(0,5),
                   (1,6),
                   (2,0),(2,2),(2,6),
                   (3,3),(3,6),
                   (4,4),(4,5)],
             '!': [(2,0),(2,1),(2,3),(2,4),(2,5),(2,6)],
             '-': [(0,3),(1,3),(2,3),(3,3),(4,3)],
             "'": [(1,3),(1,5),(2,4),(2,5)],
             '`': [(1,4),(1,5),(2,3),(2,5)],
             '"': [(1,4),(1,5),(1,6),
                   (3,4),(3,5),(3,6)],
             '/': [(0,1),(1,2),(2,3),(3,4)],
             '+': [(0,3),(1,3),
                   (2,1),(2,2),(2,3),(2,4),(2,5),
                   (3,3),(4,3)],
             '*': [(0,2),(0,4),
                   (1,3),
                   (2,1),(2,2),(2,3),(2,4),(2,5),
                   (3,3),
                   (4,2),(4,4)],
             '=': [(0,2),(1,2),(2,2),(3,2),(4,2),
                   (0,4),(1,4),(2,4),(3,4),(4,4)],
             '^': [(0,4),(1,5),(2,6),(3,5),(4,4)],
             '_': [(0,0),(1,0),(2,0),(3,0),(4,0)],
             '(': [(1,2),(1,3),(1,4),
                   (2,1),(2,5),
                   (3,0),(3,6)],
             ')': [(1,0),(1,6),
                   (2,1),(2,5),
                   (3,2),(3,3),(3,4)],
             '[': [(2,0),(2,1),(2,2),(2,3),(2,4),(2,5),(2,6),
                   (3,0),(3,6)],
             ']': [(1,0),(1,6),
                   (2,0),(2,1),(2,2),(2,3),(2,4),(2,5),(2,6)],
             '{': [(1,3),
                   (2,1),(2,2),(2,4),(2,5),
                   (3,0),(3,6),
                   (4,0),(4,6)],
             '}': [(0,0),(0,6),
                   (1,0),(1,6),
                   (2,1),(2,2),(2,4),(2,5),
                   (3,3)],
             '<': [(0,3),
                   (1,2),(1,4),
                   (2,1),(2,5),
                   (3,0),(3,6)],
             '>': [(1,0),(1,6),
                   (2,1),(2,5),
                   (3,2),(3,4),
                   (4,3)],
             '~': [(0,3),(1,4),(2,3),(3,3),(4,4)],
             '@': [(0,1),(0,2),(0,3),(0,4),(0,5),
                   (1,0),(1,6),
                   (2,0),(2,3),(2,4),(2,6),
                   (3,0),(3,2),(3,5),(3,6),
                   (4,3),(4,4),(4,5)],
             '#': [(0,2),(0,4),
                   (1,0),(1,1),(1,2),(1,3),(1,4),(1,5),(1,6),
                   (2,2),(2,4),
                   (3,0),(3,1),(3,2),(3,3),(3,4),(3,5),(3,6),
                   (4,2),(4,4)],
             '$': [(0,4),
                   (1,1),(1,3),(1,5),
                   (2,0),(2,1),(2,3),(2,5),(2,6),
                   (3,1),(3,3),(3,5),
                   (4,2)],
             '%': [(0,1),(0,4),(0,5),
                   (1,2),(1,4),(1,5),
                   (2,3),
                   (3,1),(3,2),(3,4),
                   (4,1),(4,2),(4,5)],
             '&': [(0,1),(0,2),
                   (1,0),(1,3),(1,4),(1,5),
                   (2,0),(2,2),(2,3),(2,6),
                   (3,1),(3,6),
                   (4,0),(4,2),(4,5)],
             ' ': []}

##                  [(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),
##                   (1,0),(1,1),(1,2),(1,3),(1,4),(1,5),(1,6),
##                   (2,0),(2,1),(2,2),(2,3),(2,4),(2,5),(2,6),
##                   (3,0),(3,1),(3,2),(3,3),(3,4),(3,5),(3,6),
##                   (4,0),(4,1),(4,2),(4,3),(4,4),(4,5),(4,6)]

CHARS = {(4,5): CHARS_4_5, (6,7): CHARS_6_7}

# set up kerning
KERNING = dict()
WIDTH = dict()
for charset in CHARS.keys() :
    for char in CHARS[charset].keys() :
        minx = [1000000 for i in range(0, charset[1])]
        maxx = [-1 for i in range(0, charset[1])]
        for elt in CHARS[charset][char] :
            minx[elt[1]] = min(minx[elt[1]], elt[0])
            maxx[elt[1]] = max(maxx[elt[1]], elt[0])
            if not KERNING.has_key(charset) :
                KERNING[charset] = dict()
            KERNING[charset][char] = (minx, maxx)
            if not WIDTH.has_key(charset) :
                WIDTH[charset] = dict()
            WIDTH[charset][char] = max(maxx) - min(minx)
            if WIDTH[charset][char] <= 0 :
                WIDTH[charset][char] = 0
                KERNING[charset][char] = ([0 for i in range(0, charset[1])],
                                          [0 for i in range(0, charset[1])])
            
if __name__ == "__main__" :
    import dmx
    write(dmx.getDefaultPanel(), "Hi, Tep", size=(6,7), show=True, color=(0,0.4,0))
