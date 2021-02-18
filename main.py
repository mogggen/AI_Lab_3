import terrain
from turtle import Turtle, Screen
import time

karta = terrain.perlinMap(2)

WIDTH, HEIGHT = 1000, 1000
s = 10
screen = Screen()
screen.setup(WIDTH, HEIGHT)
screen.setworldcoordinates(0, HEIGHT, WIDTH, 0)
screen.tracer(0, 0)

#destination
def rect(p):
    tur = Turtle()
    screen.colormode(255)
    
    #setters
    tur.ht()
    tur.up()
    tur.speed(0)
    for i in p:
        if str.islower(i[2]): continue
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
    

# T = Träd (5 st träd)
# V = Vatten (UW)
# G = Sumpmark (0.5 m/s)
# M = Mark (1 m/s)
def getColor(c):
    if c == 'T':
        return 13, 77, 18
    elif c == 'V':
        return 14, 113, 194
    elif c == 'G':
        return 77, 66, 26
    elif c == 'M':
        return 212, 175, 42
    elif c == 'B':
        return 125, 125, 122
    elif c == 'W':
        return 214, 92, 11

def drawMap(karta):
    global s
    nodes = []
    
    for c in karta:
        nodes += [(c[0] * s, c[1] * s, karta[c][1])]
    rect(nodes)

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