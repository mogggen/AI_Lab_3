from perlin_noise import PerlinNoise
import math
import time
import random as R
terrain = open("Map.txt", 'w')
karta = {}
occupied = ()

# AIs
# 0 = arbetare
# 1 = upptäckare
# 2 = soldater
# 3 = hantverkare

# buildings
# 4 = Kolmila
# 5 = Smedja
# 6 = Smältverk
# 7 = Träningsläger

# terrain properties
# I = järnmalm (60 st totalt)
# T = Träd (5 st träd) genereras varje sekund

# terrain type
# lowercase = undiscovered land
# V = Vatten (0 m/s)
# B = Berg (0 m/s)
# G = Sumpmark (0.5 m/s)
# M = Mark (1 m/s)

t = 'v', 'b', 'g', 'm'

def perlinMap(oct):
    print("Generating noise...")
    temp = int(time.time())
    print(temp)
    noise = PerlinNoise(octaves=oct, seed = temp)
    pic = [[noise([i/100, j/100]) for j in range(100)] for i in range(100)]
    for y in enumerate(pic):
        for x in enumerate(y[1]):
            karta[x[0], y[0]] = t[round(x[1] * len(t))] * 2 #(Neighbour)
    
    placeMaterial("i", 60)

    placeMaterial("W", 50)

    #placeMaterial("t", 100)
    
    return karta

def placeMaterial(mat, amount):
    global occupied
    occupied += (mat,)
    where = R.randint(0, len(karta) - 1)
    x, y = where % 100, where // 100
    while amount:
        where = R.randint(0, len(karta) - 1)
        x, y = where % 100, where // 100
        if karta[x, y][1] not in (t[:2] + occupied):
            karta[x, y] = karta[x, y][0] + mat
            amount -= 1