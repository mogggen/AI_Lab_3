from perlin_noise import PerlinNoise
import math
import random as R
terrain = open("Map.txt", 'w')
# T = Träd (5 st träd)
# V = Vatten (0 m/s)
# G = Sumpmark (0.5 m/s)
# M = Mark (1 m/s)
# B = Berg (0 m/s)
t = 'T', 'V', 'G', 'M', 'B'
trees = 0
def makeTerrain():
    for f in range(10000):
        if f % 100 == 0 and f != 0: terrain.write('\n')
        terrain.write(R.choice(t))

def perlinMap(oct):
    noise = PerlinNoise(octaves=oct)
    pic = [[noise([i/100, j/100]) for j in range(100)] for i in range(100)]
    
    for y in pic:
        terrain.write('\n')
        for x in y:
            if t[round(x * len(t))] == 'T' and trees < 60:
                trees += 1
                terrain.write(t[round(x * len(t))])
            else:
                terrain.write(t[round((x - 1) * len(t))])