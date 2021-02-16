import random as R
terrain = open("Map.txt", 'w')
# T = Träd (5 st träd)
# V = Vatten (UW)
# G = Sumpmark (0.5 m/s)
# M = Mark (1 m/s)
t = 'T', 'V', 'G', 'M'
def makeTerrain():
    for _ in range(10000):
        if _ % 100 == 0 and _ != 0: terrain.write('\n')
        terrain.write(R.choice(t))
