import random as R
import terrain


def placeMaterial(mat, amount):
    while amount:
        where = R.randint(0, 9999)
        x, y = where % 100, where // 100
        if terrain.karta[x // 10, y // 10][0] not in terrain.non_walkables:
            if mat in ('0', '1', '2', '3'):
                terrain.karta[x, y] = [str(terrain.karta[x, y][0]).upper() + mat]
            else:
                terrain.karta[x // 10, y // 10] = [terrain.karta[x, y][0] + mat]
            amount -= 1
