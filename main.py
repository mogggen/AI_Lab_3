import terrain
import pygame
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

pygame.init()
screen = pygame.display.set_mode((1000, 1000))



karta = terrain.InitMap()

terr = 'V', 'B', 'G', 'M', 'T'
buil = '4', '5', '6', '7' # placed on 'M'

NPCs = '0', '1', '2', '3' # can't share position
mats = 'O', 'W'
prod = 'I', 'C' # maybe invisable at all time
wepn = 'S', # maybe invisable at all time

WIDTH, HEIGHT = 1000, 1000
s = 10
nodesGG = []

#destination
def Building(p):
    for i in p:
        if str.islower(i[2]): continue
        x = i[0]
        y = i[1]
        c = i[2]
        
        getColor(c)

def rect(p):
    #setters
    for i in p:
        if str.islower(i[2]): continue
        x = i[0]
        y = i[1]
        c = i[2]
        
        getColor(c)
        rect = pygame.Rect(x, y, s, s)
        pygame.draw.rect(screen, getColor(c), rect, 1)
        screen.fill(getColor(c), rect)
    pygame.display.flip()

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
    
    print(len(explorers))
    for e in explorers:
        nodes += [(e[0] * s, e[1] * s, karta[e][0][0])]
        #for c in karta[e][1:]:
        #    if renderPos(c) in nodes:
        #        nodes += renderPos(c)
    rect(nodes)

def reveal(g, first=False):
    nodes = []
    r = (1, 1), (0, 1), (1, 0), (-1, 1), (1, -1), (-1, 0), (0, -1), (-1, -1)
    for n in r:
        pos = g[0] + n[0], g[1] + n[1]
        if not 0 <= pos[0] < 100 or not 0 < pos[1] < 100: continue
        #finalversion = karta[g][0][1] == NPCs[not first]


        if karta[g][0][1] in (NPCs[1], (NPCs[0],)[:first]):
            if (pos[0] * s, pos[1] * s, str(karta[pos][0][1]).upper()) not in nodes:
                nodes += [(pos[0] * s, pos[1] * s, str(karta[pos][0][1]).upper())]
            karta[pos][0] = str(karta[pos][0][0]).upper() + karta[pos][0][1]
    return nodes

def findNPCs(first=False):
    nodes = []
    for g in karta:
        if karta[g][0][1] not in NPCs: continue
        elif karta[g][0][1] == NPCs[0]: workers.append(g)
        elif karta[g][0][1] == NPCs[1]: explorers.append(g)
        elif karta[g][0][1] == NPCs[2]: soldiers.append(g)
        elif karta[g][0][1] == NPCs[3]: craftsmen.append(g)
        
        nodes += reveal(g, first)
    rect(nodes)

findNPCs(True)
drawMap()


def find(g):
    global nodesGG
    if karta[g][0][0].upper() not in terr[3:5]: return
    for neighboors in karta[g][1:]:
        print(karta[g])
        if neighboors not in nodesGG:
            nodesGG += [(neighboors[0] * s, neighboors[1] * s, karta[neighboors][0][0])]
            find(neighboors)
        return

#find(workers[0])
print(nodesGG)
print("done")
#rect(nodesGG)
#input()

#input(workers)
#input(explorers)
#input(soldiers)
#input(craftsmen)

def move(pos, to):
    curr = karta[pos][0][1]
    karta[pos][0] = karta[pos][0][0] * 2
    karta[to][0] = karta[to][0][0] + curr # pre connect everything in connectPath()
    rect(reveal(to))
    #drawMap()

# Grade
# 200 st '*C'
# 20 st '*I'
# 20 st '*2'
def tick():
    #r = ((1, 1), (0, 1), (1, 0), (-1, 1), (1, -1), (-1, 0), (0, -1), (-1, -1)) # check neighbours instead
    for _ in range(len(workers)):
        pos = explorers.pop(0)
        to = terrain.R.choice(karta[pos][1:])
        if 0 <= to[0] < 100 and 0 <= to[1] < 100:
            move(pos, to)
        explorers.append(to)
    
    for _ in range(len(explorers)):
        pos = explorers.pop(0)
        to = terrain.R.choice(karta[pos][1:])
        if 0 <= to[0] < 100 and 0 <= to[1] < 100:
            move(pos, to)
        explorers.append(to)
    
while True:
    enterence = time.time()
    tick()
    finish = time.time()
    #print(finish - enterence)
    print(len(explorers))
    #time.sleep(1 - (finish - enterence))