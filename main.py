import terrain
import agent
import color
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

xy1 = 15.3, 15.3
xy2 = 10.0, 9.3
# more than two agents are only necessarily when scaling the simulation (divide and conquer)



# destination
def player(p):
    for i in p:
        x = int(i[0] * s)
        y = int(i[1] * s)
        c = i[2].upper()
        square = pygame.Rect(x, y, 2, 2)
        pygame.draw.rect(screen, color.terrainColor[c], square, 1)
        screen.fill(color.terrainColor[c], square)


def rect(p):
    for i in p:
        if str.islower(i[2]):
            continue
        x = i[0] * s
        y = i[1] * s
        c = i[2].upper()
        square = pygame.Rect(x, y, s, s)
        pygame.draw.rect(screen, color.terrainColor[c], square, 1)
        screen.fill(color.terrainColor[c], square)


def connect():
    xy = 0, 0
    while xy[0] < 100 and xy[1] < 100:
        for g in karta[xy][1:]:
            newC = getColor((karta[g[:2]][0]).upper())
            pygame.draw.aaline(screen, newC, (xy[0] * s + s / 2, xy[1] * s + s / 2), (g[0] * s + s / 2, g[1] * s + s / 2), 1)
        xy = (xy[0] + 1, xy[1]) if xy[0] != 99 else (0, xy[1] + 1)


def updateMap():
    p = []
    agents = [(xy1[0], xy1[1], 'V'), (xy2[0], xy2[1], 'V')]
    karta[int(xy1[0]), int(xy1[1])][0] = (karta[int(xy1[0]), int(xy1[1])][0]).upper()
    for g in karta:
        p.append(g + (karta[g][0],))

    rect(p)

    player(agents)

    # connect()

    pygame.display.flip()



straightDelay = 0
diagonalDelay = 0
# loop
while True:
    if time.time() > straightDelay:
        if (karta[int(xy1[0]), int(xy1[1])][0]).upper() not in (terrain.walkables[0]).upper():
            straightDelay = .1
        else:
            straightDelay = 2.0
        xy1 = round(xy1[0] + .1, 1), xy1[1]
        player([(xy1[0], xy1[1], 'V')])
        straightDelay = time.time() + straightDelay
        karta[int(xy1[0]), int(xy1[1])][0] = (karta[int(xy1[0]), int(xy1[1])][0]).upper()
        #print(karta[int(xy1[0]), int(xy1[1])][0])

    if time.time() > diagonalDelay:
        if (karta[int(xy2[0]), int(xy2[1])][0]).upper() not in (terrain.walkables[0]).upper():
            diagonalDelay = .14
        else:
            diagonalDelay = 2.80
        xy2 = round(xy2[0] + .1, 1), round(xy2[1] + .1, 1)
        player([(xy2[0], xy2[1], 'V')])
        diagonalDelay = time.time() + diagonalDelay
        karta[int(xy2[0]), int(xy2[1])][0] = (karta[int(xy2[0]), int(xy2[1])][0]).upper()
        #print(karta[int(xy2[0]), int(xy2[1])][0])
    updateMap()
