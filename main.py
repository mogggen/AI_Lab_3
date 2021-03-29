import terrain
import fsm
import agent
import pathfinding
import pygame
import time


class Point:
    def __init__(self, p):
        self.x = p[0]
        self.y = p[1]

    def __abs__(self):
        x = abs(self.x)
        y = abs(self.y)

    def __len__(self, o):
        return ((self.x - o.x)**2 + (self.y - o.y)**2)**.5

    def __add__(self, o):
        self.x += o.x
        self.y += o.y

    def __sub__(self, o):
        self.x -= o.x
        self.y -= o.y

    def __eq__(self, o):
        return self.x == o.x and self.y == o.y

    def __ne__(self, o):
        return self.x != o.x or self.y != o.y


workers = []  # '0' # no clue
explorers = []  # '1' 3-12 maybe??
craftsmen = []  # '6' 1 for building and 3 for operating them.

trees = []  # 'T', yields 5 'W' after 30 seconds.
ironOre = []  # 'O', 'o' when carried.

wood = []  # 'W', 'w' when carried.
charCole = []  # 'C', 'c' when carried.
ironIngots = []  # 'I', 'i' when carried.

pygame.init()
screen = pygame.display.set_mode((1000, 1000))

karta = terrain.InitMap()

terr = 'V', 'B', 'G', 'M', 'T'
buil = '4', '5', '6', '7'  # placed on 'M'

NPCs = '0', '1', '2', '3'  # can't share position
mats = 'O', 'W'

WIDTH, HEIGHT = 1000, 1000
s = 10
nodesGG = []


# destination
def Building(p):
    for i in p:
        if str.islower(i[2]): continue
        x = i[0]
        y = i[1]
        c = i[2]

        getColor(c)


def rect(p):
    # setters
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


def drawMap():
    global karta
    nodes = []

    print(len(explorers))
    for e in explorers:
        nodes += [(e[0] * s, e[1] * s, karta[e][0][0])]
        # for c in karta[e][1:]:
        #    if renderPos(c) in nodes:
        #        nodes += renderPos(c)
    rect(nodes)


def reveal(g, first=False):
    nodes = []
    r = (1, 1), (0, 1), (1, 0), (-1, 1), (1, -1), (-1, 0), (0, -1), (-1, -1)
    for n in r:
        pos = g[0] + n[0], g[1] + n[1]
        if not 0 <= pos[0] < 100 or not 0 < pos[1] < 100:
            continue
        # finalversion = karta[g][0][1] == NPCs[not first]

        if karta[g][0][1] in (NPCs[1], (NPCs[0],)[:first]):
            if (pos[0] * s, pos[1] * s, str(karta[pos][0][1]).upper()) not in nodes:
                nodes += [(pos[0] * s, pos[1] * s, str(karta[pos][0][1]).upper())]
            karta[pos][0] = str(karta[pos][0][0]).upper() + karta[pos][0][1]
    return nodes


def findNPCs(first=False):
    nodes = []
    for g in karta:
        if karta[g][0] not in NPCs:
            continue
        elif karta[g][0] == NPCs[0]:
            workers.append(g)
        elif karta[g][0] == NPCs[1]:
            explorers.append(g)
        elif karta[g][0] == NPCs[3]:
            craftsmen.append(g)
    rect(nodes)


findNPCs(True)
drawMap()


# input(workers)
# input(explorers)
# input(craftsmen)

def move(pos, to):
    curr = karta[pos][0][1]
    karta[pos][0] = karta[pos][0][0] * 2
    karta[to][0] = karta[to][0][0] + curr  # pre connect everything in connectPath()
    rect(reveal(to))
    # drawMap()


# Grade
# 200 st '*C'
# 20 st '*I'
# 20 st '*2'
def tick():
    # r = ((1, 1), (0, 1), (1, 0), (-1, 1), (1, -1), (-1, 0), (0, -1), (-1, -1)) # check neighbours instead
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
    # print(finish - enterence)
    print(len(explorers))
    # time.sleep(1 - (finish - enterence))
