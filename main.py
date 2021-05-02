import terrain
import agent
import pygame
import time

workers = []  # '0' # no clue
explorers = []  # '1' 3-12 maybe??
craftsmen = []  # '3'

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

NPCs = '0', '1', '2', '3'  # can share position
mats = 'O', 'W'
prod = 'I', 'C'  # maybe invisible at all time

WIDTH, HEIGHT = 1000, 1000
s = 10

xy1 = 10.3, 10.3
xy2 = 10.0, 9.3
# more than two agents are only necessarily when scaling the simulation (divide and conquer)



# destination
def player(p):
    for i in p:
        x = int(i[0] * s)
        y = int(i[1] * s)
        c = i[2].upper()
        square = pygame.Rect(x, y, 2, 2)
        pygame.draw.rect(screen, getColor(c), square, 1)
        screen.fill(getColor(c), square)


def rect(p):
    for i in p:
        if str.islower(i[2]):
            continue
        x = i[0] * s
        y = i[1] * s
        c = i[2].upper()
        square = pygame.Rect(x, y, s, s)
        pygame.draw.rect(screen, getColor(c), square, 1)
        screen.fill(getColor(c), square)


def connect():
    xy = 0, 0
    while xy[0] < 100 and xy[1] < 100:
        for g in karta[xy][1:]:
            newC = getColor((karta[g[:2]][0]).upper())
            pygame.draw.aaline(screen, newC, (xy[0] * s + s / 2, xy[1] * s + s / 2), (g[0] * s + s / 2, g[1] * s + s / 2), 1)
        xy = (xy[0] + 1, xy[1]) if xy[0] != 99 else (0, xy[1] + 1)


def getColor(c):
    # terr
    if c == 'T':
        return [13, 77, 18]
    elif c == 'V':
        return [14, 113, 194]
    elif c == 'G':
        return [77, 66, 26]
    elif c == 'M':
        return 212, 175, 42
    elif c == 'B':
        return [125, 125, 122]

    # NPCs
    elif c in ('0', 'i', 'w', 'c', 'o'):
        return [214, 92, 11]
    elif c == '1':
        return [177, 204, 41]
    elif c in ('2', 's'):
        return [255, 0, 153]
    elif c == '3':  # lives in the corresponding building
        return [69, 209, 200]

    # Iron
    elif c == 'I':  # maybe invisible at all time
        return [165, 198, 204]
    elif c == 'O':
        return [48, 111, 122]

    # sword
    elif c == 'S':  # maybe invisible at all time
        return [255, 0, 0]

    # wood
    elif c == 'W':
        return [158, 75, 44]
    elif c == 'C':  # maybe invisible at all time
        return [22, 22, 22]


def updateMap():
    p = []
    agents = [(xy1[0], xy1[1], 'V'), (xy2[0], xy2[1], 'V')]
    karta[int(xy1[0]), int(xy1[1])][0] = (karta[int(xy1[0]), int(xy1[1])][0]).upper()
    for g in karta:
        p.append(g + (karta[g][0],))

    rect(p)

    player(agents)

    #connect()

    pygame.display.flip()


def reveal(g, first=False):
    nodes = []
    r = (1, 1), (0, 1), (1, 0), (-1, 1), (1, -1), (-1, 0), (0, -1), (-1, -1)
    for n in r:
        pos = g[0] + n[0], g[1] + n[1]
        if not 0 <= pos[0] < 100 or not 0 < pos[1] < 100:
            continue
        # finalVersion = karta[g][0][1] == NPCs[not first]

        if karta[g][0][1] in (NPCs[1], (NPCs[0],)[:first]):
            if (pos[0] * s, pos[1] * s, str(karta[pos][0][1]).upper()) not in nodes:
                nodes += [(pos[0] * s, pos[1] * s, str(karta[pos][0][1]).upper())]
            karta[pos][0] = str(karta[pos][0][0]).upper() + karta[pos][0][1]
    return nodes


#drawMap()


def move(pos, to):
    # if time.time()

    rect(reveal(to))
    # drawMap()


# Grade
# 200 st '*C'
def tick():
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


straightDelay = 0
diagonalDelay = 0
# loop
while True:
    if time.time() > straightDelay:
        xy1 = round(xy1[0] + .1, 1), xy1[1]
        player([(xy1[0], xy1[1], 'V')])
        straightDelay = time.time() + .1
        karta[int(xy1[0]), int(xy1[1])][0] = (karta[int(xy1[0]), int(xy1[1])][0]).upper()
        #print(karta[int(xy1[0]), int(xy1[1])][0])

    if time.time() > diagonalDelay:
        xy2 = round(xy2[0] + .1, 1), round(xy2[1] + .1, 1)
        player([(xy2[0], xy2[1], 'V')])
        diagonalDelay = time.time() + .14
        karta[int(xy2[0]), int(xy2[1])][0] = (karta[int(xy2[0]), int(xy2[1])][0]).upper()
        #print(karta[int(xy2[0]), int(xy2[1])][0])
    updateMap()
