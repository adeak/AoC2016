import numpy as np
from collections import defaultdict
from operator import itemgetter
from scipy import ndimage

def is_valid(x,y,c):
    if x>=0 and y>=0 and bin((x+y)**2+3*x+y+c).count('1')%2==0:
        return True
    return False

# see A* wikipedia
def day13_astar(c,finalpos):
    posnow = (1,1)
    pathlen = 0
    visited = []
    tovisit = []
    visited.append(posnow)
    tovisit.append(posnow)

    prevpos = {}
    gscore = defaultdict(lambda: 1e100)
    fscore = defaultdict(lambda: 1e100)
    gscore[posnow] = 0
    fscore[posnow] = heuristic_cost(posnow,finalpos)

    while len(tovisit)>0:
        posnow = sorted([(pos,fscore[pos]) for pos in tovisit],key=itemgetter(1))[0][0]
        if posnow==finalpos:
            finalpath = reconstruct_path(prevpos,posnow)
            print('found first path with stepnum {}: {}'.format(len(finalpath)-1,finalpath))
            return finalpath
        tovisit.remove(posnow)
        visited.append(posnow)

        xl,yl = posnow
        for xn,yn in (xl+1,yl),(xl-1,yl),(xl,yl+1),(xl,yl-1):
            if not is_valid(xn,yn,c) or (xn,yn) in visited:
                continue
            tentative_gscore = gscore[posnow] + 1
            if (xn,yn) not in tovisit:
                tovisit.append((xn,yn))
            elif tentative_gscore >= gscore[(xn,yn)]:
                # discard path
                continue
            # best path so far
            prevpos[(xn,yn)] = posnow
            gscore[(xn,yn)] = tentative_gscore
            fscore[(xn,yn)] = gscore[posnow] + heuristic_cost((xn,yn),finalpos)
    return 'A* failed :('

def heuristic_cost(posnow,finalpos):
    return abs(finalpos[0]-posnow[0]) + abs(finalpos[1]-posnow[1]) #~ straight line

def reconstruct_path(prevpos,posnow):
    allpath = [posnow]
    while posnow in prevpos:
        posnow = prevpos[posnow]
        allpath.append(posnow)
    return allpath


def day13b(c,stepnum):
    posnow = (1,1)
    maze = np.vectorize(lambda x,y,c=c:is_valid(x,y,c),otypes=[bool])(*np.ogrid[:stepnum+1,:stepnum+1])

    paths = np.zeros((stepnum+1,stepnum+1),dtype=bool)
    paths[posnow] = True
    for k in range(stepnum):
        paths = ndimage.binary_dilation(paths,mask=maze)
        print('number of sites after {} steps: {}'.format(k,paths.sum()))
    print('done with steplen {}.'.format(paths.sum()))
