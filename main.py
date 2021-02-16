import terrain
import turtle
import time

terrain.makeTerrain()
print("done")
s = 10

#destination
def rect(p):
    tur = turtle.Turtle()
    
    #setters
    tur.ht()
    tur.up()
    tur.speed(0)
    for i in p:
        if i[2] in ("M", "\n"): continue
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

foo = open("Map.txt", 'r')
karta = foo.read()

# T = Träd (5 st träd)
# V = Vatten (UW)
# G = Sumpmark (0.5 m/s)
# M = Mark (1 m/s)
def getColor(c):
    if c == 'T':
        return "green"
    elif c == 'W':
        return "blue"
    elif c == 'G':
        return "brown"
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
            y -= s
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