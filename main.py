import terrain
from turtle import Turtle, Screen
import time

workers = [] # '0' # no clue
explorers = [] # '1' 3-12 maybe??
soldiers = [] # '2' # perhaps 20, best case senario
craftsmen = [] # '3' # generate three one for each corresponding building,
                     # then they continue to maintain each faculty,
                     # for a total of three craftsmen.

trees = [] # 'T', yields 5 'W' after 30 seconds.
ironOre = [] # 'O', 'o' when carried.

wood = [] # 'W', 'w' when carried.
charCole = [] # 'C', 'c' when carried.
ironIngots = [] # 'I', 'i' when carried.


karta = terrain.InitMap()

terr = 'V', 'B', 'G', 'M', 'T'
buil = '4', '5', '6', '7' # placed on 'M'

NPCs = '0', '1', '2', '3' # can't share position
mats = 'O', 'W'
prod = 'I', 'C' # maybe invisable at all time
wepn = 'S', # maybe invisable at all time

WIDTH, HEIGHT = 1000, 1000
s = 10
screen = Screen()
screen.setup(WIDTH, HEIGHT)
screen.setworldcoordinates(0, HEIGHT, WIDTH, 0)
screen.tracer(0, 0)

#destination
def Building(p):
    tur = Turtle()
    screen.colormode(255)
    input()
    #setters
    #tur.ht()
    #tur.up()
    tur.speed(0)
    for i in p:
        if str.islower(i[2]): continue
        x = i[0]
        y = i[1]
        c = i[2]
        
        tur.fillcolor(getColor(c))

        #position
        tur.goto(x - s / 2, y)

        #fill rec
        tur.begin_fill()
        for _ in range(4):
            tur.fd(s)
            tur.rt(45)
        tur.end_fill()
    screen.update()

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
    #terr
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

    #NPCs
    elif c in ('0', 'i', 'w', 'c', 'o'):
        return 214, 92, 11
    elif c == '1':
        return 177, 204, 41
    elif c in ('2', 's'):
        return 255, 0, 153
    elif c == '3': # lives in the corresponding building
        return 69, 209, 200

    #Iron
    elif c == 'I': # maybe invisable at all time
        return 165, 198, 204
    elif c == 'O':
        return 48, 111, 122
    
    #sword
    elif c == 'S': # maybe invisable at all time
        return 255, 0, 0
    
    #wood
    elif c == 'W':
        return 158, 75, 44
    elif c == 'C': # maybe invisable at all time
        return 22, 22, 22

def drawMap():
    global karta
    nodes = []
    
    for c in karta:
        if str(karta[c][0][0]).islower(): continue
        nodes += [(c[0] * s, c[1] * s, karta[c][0][1])]
    rect(nodes)

def Refresh(g, first=""):
    nodes = []
    r = ((1, 1), (0, 1), (1, 0), (-1, 1), (1, -1), (-1, 0), (0, -1), (-1, -1))
    for n in r:
        try:
            pos = g[0] + n[0], g[1] + n[1]

            if karta[g][0][1] in (NPCs[1] + (first),):
                nodes += [(pos[0] * s, pos[1] * s, str(karta[pos][0][0]).upper())]
                karta[pos][0] = str(karta[pos][0][0]).upper() + karta[pos][0][1]
            
            #check if it's neighbour
            if karta[pos][0][0] in terr[2:4]:
                karta[g] += [pos]
        except KeyError:
            continue
    return nodes

def connectPath(first=""):
    nodes = []
    for g in karta:
        if karta[g][0][1] not in NPCs: continue
        elif karta[g][0][1] in NPCs[0]: workers.append(g)
        elif karta[g][0][1] in NPCs[1]: explorers.append(g)
        elif karta[g][0][1] in NPCs[2]: soldiers.append(g)
        elif karta[g][0][1] in NPCs[0]: craftsmen.append(g)
        
        nodes += Refresh(g, first)
    rect(nodes)    

connectPath(NPCs[0])
drawMap()
#input(workers)
#input(explorers)
#input(soldiers)
#input(craftsmen)

def move(pos, to):
    temp = karta[pos][0][1]
    karta[pos][0] = karta[pos][0][0] * 2
    new = pos[0] + to[0], pos[1] + to[1]
    karta[new][0] = karta[new][0][0] + temp # connect revealed ground
    explorers.append(new)

# Grade
# 200 st '*C'
# 20 st '*I'
# 20 st '*2'
def tick():
    r = ((1, 1), (0, 1), (1, 0), (-1, 1), (1, -1), (-1, 0), (0, -1), (-1, -1))
    for _ in range(len(explorers)):
        move(explorers.pop(0), terrain.R.choice(r))
    connectPath()
    drawMap()
    
while True:
    enterence = time.time()
    tick()
    time.sleep(1 - (time.time() - enterence))