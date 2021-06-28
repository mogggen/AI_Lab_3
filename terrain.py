import math
import time
import random as R
import pygame

import color
import main

terrain = open("Map.txt", 'r')
karta = {}
occupied = ()

# Agents : karta[key][0][1]
# 0 = arbetare red : eller O, I, T, C om dem bär på respektive matrial
# 1 = upptäckare : limeyellow
# 2 = soldater pink
# 3 = hantverkare lightblue

# terrain properties : karta[key][0][1]
# i = järnmalm (60 st totalt)

# buildings : karta[key][0][0] sjärnformade, med samma färg som arbetarna.
# 4 = Kolmila : '44' empty, '43' operational
# 5 = Smedja : '55' empty, '53' operational
# 6 = Smältverk : '66' empty, '63' operational
# 7 = Träningsläger : '77' empty, '73' operational

# terrain type : karta[key][0][0]
# lowercase = undiscovered land
# V = Vatten (0 m/s)
# B = Berg (0 m/s)
# G = Sumpmark (0.5 m/s)
# M = Mark (1 m/s)
# T = Träd (? m/s) (5 st träd / 30 sek) 

non_walkables = 'v', 'b'
walkables = 'm', 't', 'g'


def InitMap():
    h = terrain.read()
    chars = h[:]
    chars = str(chars).replace("\n", "").lower()
    h = str(h).split('\n')
    for y in enumerate(h):
        for x in enumerate(y[1]):
            karta[x[0], y[0]] = [chars[x[0] + y[0] * len(y[1])]]
    walkableEdges()
    return karta


def findTrees(land):
    global karta
    for g in karta:
        if karta[g][0] == 't':
            land.trees = 5
        drawTrees(g, land.trees)


def drawTrees(pos: tuple, amount):
    if not amount:
        return
    loc = [29, 43, 75, 54, 31]
    for T in loc[:amount]:  # FIXME main.screen causes circular import
        square = pygame.Rect(pos[0] * 10 + T // 10, pos[1] * 10 + T % 10, 2, 2)
        pygame.draw.rect(main.screen, color.terrainColor['T'], square, 1)
        main.screen.fill(color.terrainColor['T'], square)

def walkableEdges():
    r = (1, 1), (0, 1), (1, 0), (-1, 1), (1, -1), (-1, 0), (0, -1), (-1, -1)
    global karta
    for g in karta:
        for n in r:
            pos = g[0] + n[0], g[1] + n[1]
            if not 0 <= pos[0] < 100 or not 0 <= pos[1] < 100 or karta[pos] in non_walkables:
                continue

            if karta[pos][0] in walkables:
                v = 1
                if not (n[0] + n[1]) % 2:
                    v = round((2 * v ** 2) ** .5, 1)
                    if karta[pos][0] not in walkables[0]:
                        v = round(2 * v, 1)
                karta[g] += [pos + (v,)]


def findScoutGoal():
    while True:
        where = R.randint(0, 9999)
        scoutGoal = where % 100, where // 100
        if karta[scoutGoal][0] in ("m", "g"):
            return scoutGoal


def placeAgents():
    r = (1, 1), (0, 1), (1, 0), (-1, 1), (1, -1), (-1, 0), (0, -1), (-1, -1), (0, 0)
    while True:
        where = R.randint(0, 9999)
        x, y = where % 100, where // 100
        if karta[x, y][0] in ("m", "g"):
            for dx, dy in r:
                u = x + dx, y + dy
                karta[u] = [karta[u][0].upper()]
            return x, y
