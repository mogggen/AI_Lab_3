import terrain
from turtle import Turtle, Screen
import time

terrain.perlinMap(5)
WIDTH, HEIGHT = 1000, 1000
s = 10
screen = Screen()
screen.setup(WIDTH, HEIGHT)
screen.setworldcoordinates(0, HEIGHT, WIDTH, 0)
screen.tracer(0, 0)

#destination
def rect(p):
    tur = Turtle()
    
    #setters
    tur.ht()
    tur.up()
    tur.speed(0)
    for i in p:
        if i[2] in ("\n"): continue
        x = i[0]
        y = i[1]
        c = i[2]
        
        #continue
        tur.fillcolor(getColor(c))

        #position
        tur.goto(x - s / 2, y - s / 2)

        #fill rec
        tur.begin_fill()
        
        tur.setx(x + s / 2)
        tur.sety(y + s / 2)
        tur.setx(x - s / 2)
        tur.sety(y - s / 2)
        tur.end_fill()
    screen.update()

foo = open("Map.txt", 'r')
karta = foo.read()

# T = Träd (5 st träd)
# V = Vatten (UW)
# G = Sumpmark (0.5 m/s)
# M = Mark (1 m/s)
def getColor(c):
    if c == 'T':
        return "green"
    elif c == 'V':
        return "blue"
    elif c == 'G':
        return "brown"
    elif c == 'M':
        return "maroon"
    elif c == 'B':
        return "black"
    else:
        return "Unknown token"

def drawMap(karta):
    global s
    nodes = []
    x = 0
    y = 0
    
    for c in karta:
        if c == '\n':
            x = 0
            y += s
        else:
            nodes += [(x, y, c)]
            x += s
        
    rect(nodes)
    return nodes

def makeGraph(karta):
    graph = {}
    x = 0
    y = 0
    #create grid
    for k in karta:
        if k == '\n':
            x = 0
            y += 1
        else:
            graph[(x, y)] = [k]
            x += 1
    return graph

drawMap(karta)
input()