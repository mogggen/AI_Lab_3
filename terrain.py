from perlin_noise import PerlinNoise
import math
import time
import random as R
terrain = open("Map.txt", 'r')
karta = {}
occupied = ()

# AIs : karta[key][0][1]
# 0 = arbetare red : eller O, I, T, C om dem bär på respektive matrial
# 1 = upptäckare : limeyellow
# 2 = soldater pink
# 3 = hantverkare lightblue

# terrain properties : karta[key][0][1]
# i = järnmalm (60 st totalt)
# s = Svärd (för att göra soldater) (gör max 20 alltid)

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

t = 'V', 'B', 'G', 'M'
t = 'v', 'b', 'g', 'm'

def InitMap():
    h = terrain.read()
    chars = h[:]
    chars = str(chars).replace("\n", "").lower()
    h = str(h).split('\n')
    for y in enumerate(h):
        for x in enumerate(y[1]):
            karta[x[0], y[0]] = [chars[x[0] + y[0] * len(y[1])] * 2]

    placeMaterial("0", 0)
    placeMaterial("1", 50)
    placeMaterial('I', 60)
    walkableEdges()
    return karta

def walkableEdges():
    r = (1, 1), (0, 1), (1, 0), (-1, 1), (1, -1), (-1, 0), (0, -1), (-1, -1)
    global karta
    waitTime = 0
    for g in karta:
        for n in r:
            pos = g[0] + n[0], g[1] + n[1]
            if not 0 <= pos[0] < 100 or not 0 < pos[1] < 100: continue
            if t[2] in (str(karta[pos][0][0]).upper()):
                waitTime += 10
                if t[2] in (str(karta[pos[0], g[1]][0][0]).upper(),
                str(karta[g[0], pos[1]][0][0]).upper()):
                    waitTime += 4
            elif t[3] in (str(karta[pos][0][0]).upper()):
                waitTime += 20
                if t[3] in (str(karta[pos[0], g[1]][0][0]).upper(),
                str(karta[g[0], pos[1]][0][0]).upper()):
                    waitTime += 8
            karta[g] += [pos]
            waitTime = 0

def placeMaterial(mat, amount):
    global occupied
    occupied += (mat,)
    where = R.randint(0, 9999)
    x, y = where % 100, where // 100
    while amount:
        where = R.randint(0, 9999)
        x, y = where % 100, where // 100
        if karta[x, y][0][1] not in (t[:2] + occupied):
            if mat in ('0', '1', '2', '3'):
                karta[x, y] = [str(karta[x, y][0][0]).upper() + mat]
            else:
                karta[x, y] = [karta[x, y][0][0] + mat]
            amount -= 1