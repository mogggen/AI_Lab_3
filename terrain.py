import math
import time
import random as R
terrain = open("Map.txt", 'r')

start = R.randint(0, 9_999)
karta = {}

# Agents
# 0 = arbetare red : eller O, I, T, C om dem bär på respektive matrial
# 1 = upptäckare : limeyellow
# 2 = soldater pink
# 3 = hantverkare lightblue

# terrain properties 
# i = järnmalm (60 st totalt)
# s = Svärd (för att göra soldater) (gör max 20 alltid)

# buildings : karta[key][0][0] sjärnformade, med samma färg som arbetarna.
#Kolmila

# terrain type : karta[key][0][0]
# lowercase = undiscovered land
# V = Vatten (0 m/s)
# B = Berg (0 m/s)
# G = Sumpmark (0.5 m/s)
# M = Mark (1 m/s)
# T = Träd (0.75 m/s) (5 st träd per ruta/ 30 sek)

unwalkables = 'v', 'b'
walkables = 'm', 'g', 't'

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

def walkableEdges():
    r = (1, 1), (0, 1), (1, 0), (-1, 1), (1, -1), (-1, 0), (0, -1), (-1, -1)
    global karta
    ms = 0
    for g in karta:
        for n in r:
            pos = g[0] + n[0], g[1] + n[1]
            if not 0 <= pos[0] < 100 or not 0 <= pos[1] < 100 or (karta[pos] in unwalkables):
                continue
            
            ms = .5 + bool(karta[pos][0] is not walkables[0]) / 2
            karta[g] += [pos + (ms,)]

