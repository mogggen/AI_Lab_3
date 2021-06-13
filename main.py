import pathfinding
from enums import GoalEnum, AgentEnum, ItemEnum
import terrain
import color
import pygame
from time import time

r = (1, 1), (0, 1), (1, 0), (-1, 1), (1, -1), (-1, 0), (0, -1), (-1, -1)

workers = []  # '0' # no clue
explorers = []  # '1' 3-12 maybe??
craftsmen = []  # '3'

trees = []  # 'T', yields 1 'W' after 30 seconds.

pygame.init()
screen = pygame.display.set_mode((1000, 1000))


class Land:
    def __init__(self, pos, terrain_enum):
        self.pos = pos
        self.terrain = terrain_enum
        self.parent = None


class Agent:
    def __init__(self, pos):
        self.pos = pos
        self.pathToGoal = []
        self.goalPos = None

        self.agentType = AgentEnum.WORKER
        self.timer = 0
        self.holding = ItemEnum.none

    # move from center to center, runs every execute
    def move(self):
        if len(self.pathToGoal):
            return
        # you have arrived at the neighbouring tile
        if self.pos == self.pathToGoal[0]:

            self.timer += pathfinding.moveCost(self.pos, self.pathToGoal.pop(0))
            #if self.pathToGoal


lands = []
karta = terrain.InitMap()


terr = 'V', 'B', 'G', 'M', 'T'
buil = '4',  # placed on 'M'

for sn in karta:
    lands.append(Land(sn, karta[sn][0]))

WIDTH, HEIGHT = 1000, 1000
s = 10

xy1 = 10, 10
xy2 = 10, 10
# more than two agents are only necessarily when scaling the simulation (divide and conquer)


# destination
def player(p):
    for i in p:
        x = i[0] * s
        y = i[1] * s
        c = i[2].upper()
        square = pygame.Rect(x + s // 2, y + s // 2, 2, 2)
        pygame.draw.rect(screen, color.terrainColor[c], square, 1)  # draw it here
        screen.fill(color.terrainColor[c], square)


def rect(p):
    for i in p:
        if str.islower(i[2]):
            continue
        x = i[0] * s
        y = i[1] * s
        c = i[2].upper()
        square = pygame.Rect(x, y, s, s)
        pygame.draw.rect(screen, color.terrainColor[c], square, 1)  # draw it here
        screen.fill(color.terrainColor[c], square)


def connect():
    xy = 0, 0
    while xy[0] < 100 and xy[1] < 100:
        for g in karta[xy][1:]:
            newC = color.terrainColor[(karta[g[:2]][0]).upper()]
            pygame.draw.aaline(screen, newC, (xy[0] * s + s / 2, xy[1] * s + s / 2), (g[0] * s + s / 2, g[1] * s + s / 2), 1)
        xy = (xy[0] + 1, xy[1]) if xy[0] != 99 else (0, xy[1] + 1)


def updateMap():
    p = []
    agents = [Agent(xy1)]
    agents = [(xy1[0], xy1[1], 'V'), (xy2[0], xy2[1], 'V')]
    for g in karta:
        p.append(g + (karta[g][0],))

    rect(p)

    player(agents)

    # connect()

    pygame.display.flip()



def exploreDistrict():
    # start with two agents: one worker, one explorer
    #def moveTowardCenterOfSquare(fromNextSquareInPath):
        

    #popUpcomingPath(forAgentToTake)

    #trees.append(newFoundTreesAsGoals)
    pass


straightDelay = 0
diagonalDelay = 0
# loop
while True:
    if time() > straightDelay:
        if (karta[xy1][0]).upper() in (terrain.walkables[0]).upper():
            straightDelay = 10
        else:
            straightDelay = 20

        xy1 = xy1[0] + 1, xy1[1]
        player([(xy1[0], xy1[1], 'V')])
        for n in r + ((0, 0),):
            p1 = xy1[0] + n[0], xy1[1] + n[1]
            karta[p1][0] = (karta[p1][0]).upper()
        straightDelay = time() + straightDelay

    if time() > diagonalDelay:
        if (karta[xy2][0]).upper() in (terrain.walkables[0]).upper():
            diagonalDelay = 14
        else:
            diagonalDelay = 28

        xy2 = xy2[0] + 1, xy2[1] + 1
        player([(xy2[0], xy2[1], 'V')])
        for n in r + ((0, 0),):
            p2 = xy2[0] + n[0], xy2[1] + n[1]
            karta[p2][0] = (karta[p2][0]).upper()
        diagonalDelay = time() + diagonalDelay

    updateMap()
