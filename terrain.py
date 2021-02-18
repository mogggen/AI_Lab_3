from perlin_noise import PerlinNoise
import math
import random as R
terrain = open("Map.txt", 'w')

# buildings
# 0 = arbetare
# 1 = upptäckare
# 2 = soldater
# 3 = hantverkare

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

#pre-game to not have to check list {(0, 0): 'BB'} and then no neighbours, ok!
def perlinMap(oct):
    noise = PerlinNoise(octaves=oct)
    pic = [[noise([i/100, j/100]) for j in range(100)] for i in range(100)]
    karta = {}
    for y in enumerate(pic):
        for x in enumerate(y[1]):
            if x[0] % 100 == 0 and y[0] != 0:
                karta[(x[0], y[0])] = '\n' * 2
                continue
            karta[x[0], y[0]] = [t[round(x[1] * len(t))] * 2] #(Neighbour)
    
    ironOre = 60
    where = R.randint(0, len(karta) - 1)
    x, y = where % 100, where // 100
    while ironOre:
        if karta[x, y][1] in t[:2] or karta[x, y][1] == '\n':
            where = R.randint(0, len(karta) - 1)
        else:
            karta[x, y] = karta[x, y][0] + 'I' # only secound index
            ironOre -= 1

    workers = 50
    where = R.randint(0, len(karta) - 1)
    x, y = where % 100, where // 100
    while workers:
        if karta[x, y][1] in t[:2] + ['T'] or karta[x, y][1] == '\n':
            where = R.randint(0, len(karta) - 1)
        else:
            karta[x, y] = karta[x, y][0] + 'W' # only secound index
            workers -= 1
    
    for k in karta:
        terrain.write(karta[k][1])
    return karta