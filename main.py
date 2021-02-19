import terrain
from turtle import Turtle, Screen
import time

ironIngots = []
workers = []
trees = []
karta = terrain.perlinMap(1.5)
t = 'V', 'B', 'G', 'M', 'T', 'I', 'W' # worker can't share position

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
    elif c == 'I':
        return 165, 198, 204

def drawMap():
    global karta
    global s
    nodes = []
    
    for c in karta:
        nodes += [(c[0] * s, c[1] * s, karta[c][0][1])]
    rect(nodes)

def Reveal(p):
    nodes = []
    global karta



def connectPath():
    global workers
    global karta
    r = ((1, 1), (0, 1), (1, 0), (-1, 1), (1, -1), (-1, 0), (0, -1), (-1, -1))
    nodes = []
    for g in karta:
        for n in r:
            try:
                pos = g[0] + n[0], g[1] + n[1]

                #check if it's close to worker at start
                if karta[g][0][1] in t[6]:
                    workers += [g]
                    nodes += [pos[0] * s, pos[1] * s, str(karta[pos][0]).upper()[0]]
                    karta[pos][0] = str(karta[pos][0]).upper()
                
                #check if it's neighbour
                if karta[pos][0][0] in t[2:4]:
                    karta[g] += pos
            except KeyError:
                continue
            rect(nodes)
    return karta

connectPath()
drawMap()
input()

# Grade
# 200 st '*C'
# 20 st '*I'
# 20 st '*2'
def tick():
    enterence = time.time()
    