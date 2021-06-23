import enums
import pathfinding
from enums import AgentEnum, ItemEnum
import terrain
import color
import pygame
from time import time

r = (1, 1), (0, 1), (1, 0), (-1, 1), (1, -1), (-1, 0), (0, -1), (-1, -1)

charCoal = 0

# workers = []  # the rest
# explorers = []  # 3
# craftsmen = []  # 1 total

pygame.init()
WIDTH, HEIGHT = 1000, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))


class Land:
    def __init__(self, terrain_enum, trees=0):
        self.terrain = terrain_enum
        self.trees = trees  # yields 1 tree after 30 seconds


class Agent:
    def __init__(self, pos):
        self.pos = pos
        self.pathToGoal = []

        self.agentType = AgentEnum.WORKER
        self.timer = 0
        self.holding = ItemEnum.none


lands = {}
discovered = {}  # (x, y): trees
karta = terrain.InitMap()
startingPoint = terrain.placeAgents()
agents = [Agent(startingPoint[:]), Agent(startingPoint[:])]
agents[1].agentType = AgentEnum.SCOUT

terr = 'V', 'B', 'G', 'M', 'T'
buildings = 'C',  # placed on 'M'

for L in karta:
    lands[L] = Land(karta[L][0])
    if karta[L][0].upper() == terr[-1]:
        lands[L].terrain = terr[-2]
        lands[L].trees = 5

s = 10

# destination
def draw_players(p):
    for i in p:
        x, y = i.pos[0] * s + s // 2, i.pos[1] * s + s // 2
        # what type of agent should be rendered
        if i.agentType == enums.AgentEnum.WORKER:
            c = color.agentColor[0]
        elif i.agentType == enums.AgentEnum.SCOUT:
            c = color.agentColor[1]
        elif i.agentType == enums.AgentEnum.BUILDER:
            c = color.agentColor[2]
        elif i.agentType == enums.AgentEnum.MILLER:
            c = color.agentColor[3]
        else:
            print(i)
            raise NotImplementedError
        square = pygame.Rect(x + s // 2, y + s // 2, 2, 2)
        pygame.draw.rect(screen, c, square, 1)
        screen.fill(c, square)


def rect(p):
    for i in p:
        if i[2].islower():
            continue
        x = i[0] * s
        y = i[1] * s
        c = i[2].upper()
        square = pygame.Rect(x, y, s, s)
        pygame.draw.rect(screen, color.terrainColor[c], square, 1)  # draw it here
        screen.fill(color.terrainColor[c], square)


def draw_connections():
    xy = 0, 0
    while xy[0] < 100 and xy[1] < 100:
        for g in karta[xy][1:]:
            newC = color.terrainColor[(karta[g[:2]][0]).upper()]
            pygame.draw.aaline(screen, newC, (xy[0] * s + s / 2, xy[1] * s + s / 2),
                               (g[0] * s + s / 2, g[1] * s + s / 2), 1)
        xy = (xy[0] + 1, xy[1]) if xy[0] != 99 else (0, xy[1] + 1)




def update_map():
    global discovered
    global agents

    for L in lands:
        terrain.drawTrees(L, lands[L].trees)

    # find trees
    for g in karta:
        if karta[g][0].isupper():
            discovered[g] = karta[g][0]
        rect(discovered[g] + (karta[g][0],))

    draw_players(agents)

    # draw_connections()

    pygame.display.flip()


previousDeltaCalculationTime = 0
shortestTimeSpanRemaining = 0
nodesToTraverse = pathfinding.convertLandToNodes(lands)


# loop
while charCoal < 200:
    shortestTimeSpanRemaining = min(agents, key=lambda t: t.timer).timer  # to avoid race conditions
    for a in agents:
        if time() > a.timer:
            if a.agentType in (AgentEnum.WORKER, AgentEnum.SCOUT):
                if a.pathToGoal:
                    a.pos = a.pathToGoal.pop()
                    a.timer = pathfinding.moveCost(a.pos, a.pathToGoal[0]) * (1 + bool(
                        (karta[a.pos][0]).upper() in (
                            terrain.walkables[0]).upper()))
                else:
                    nodesToTraverse = pathfinding.convertLandToNodes()  # something with pos, g, h
                    a.pathToGoal = pathfinding.aStar(nodesToTraverse, a.pos, shortestTimeSpanRemaining)

                if a.agentType == AgentEnum.SCOUT:
                    for n in r + ((0, 0),):
                        neigh = a.pos[0] + n[0], a.pos[1] + n[1]
                        karta[neigh][0] = (karta[neigh][0]).upper()
                        discovered[neigh] = lands[neigh].trees
            a.timer = time() + a.timer

    update_map()
