from perlin_noise import PerlinNoise
import math
import time
import random as R
terrain = open("Map.txt", 'r')
karta = {}
occupied = ()

# AIs : karta[key][0][1]
# 0 = arbetare red : or O, I, T, C om dem bär på respektive matrial
# 1 = upptäckare : limeyellow
# 2 = soldater pink : S om det bär på svärd
# 3 = hantverkare lightblue

# buildings : karta[key][0][0] sjärnformade, med samma färg som arbetarna.
# 4 = Kolmila
# 5 = Smedja
# 6 = Smältverk
# 7 = Träningsläger

# terrain properties : karta[0][1]
# I = järnmalm (60 st totalt)
# S = Svärd

# terrain type
# lowercase = undiscovered land
# V = Vatten (0 m/s)
# B = Berg (0 m/s)
# G = Sumpmark (0.5 m/s)
# M = Mark (1 m/s)
# T = Träd (? m/s) (5 st träd / 30 sek) 

t = 'V', 'B', 'G', 'M'
t = 'v', 'b', 'g', 'm'

def getMap():
    h = terrain.read()
    chars = h[:]
    chars = str(chars).replace("\n", "").lower()
    h = str(h).split('\n')
    for y in enumerate(h):
        for x in enumerate(y[1]):
            karta[x[0], y[0]] = [chars[x[0] + y[0] * len(y[1])] * 2]

    placeMaterial("0", 10)
    placeMaterial('i', 60)
    #placeMaterial("1", 5)
    #placeMaterial("2", 20)
    #placeMaterial("3", 15)
    return karta

def placeMaterial(mat, amount):
    global occupied
    occupied += (mat,)
    where = R.randint(0, len(karta) - 1)
    x, y = where % 100, where // 100
    while amount:
        where = R.randint(0, len(karta) - 1)
        x, y = where % 100, where // 100
        if karta[x, y][0][1] not in (t[:2] + occupied):
            karta[x, y] = [karta[x, y][0][0] + mat]
            amount -= 1