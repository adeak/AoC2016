import numpy as np
from itertools import permutations

def day3(sideslist):
    sides = np.fromstring(sideslist,sep=' ').reshape(-1,3)
    return sum(np.all(list(sides[:,k1]+sides[:,k2]>sides[:,k3] for k1,k2,k3 in permutations(range(3))),axis=0))


def day3b(sideslist):
    sides = np.fromstring(sideslist,sep=' ').reshape(-1,3)
    sides = sides.T.reshape(-1,3)
    return sum(np.all(list(sides[:,k1]+sides[:,k2]>sides[:,k3] for k1,k2,k3 in permutations(range(3))),axis=0))