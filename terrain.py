import math
import time
import random as R

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
    # placeAgents()
    walkableEdges()
    return karta


def placeTrees(land):
    global karta
    for g in karta:
        if karta[g][0] == 't':
            karta[g][0] = 'm'.upper()
            land.trees = [29, 43, 75, 54, 31]

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
