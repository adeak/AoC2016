import numpy as np
from scipy import ndimage
# for A* part 1 alternative:
from collections import defaultdict

def day13(c,finalpos=None,stepnum=None):
    '''
    Inputs: c int primary input code
            finalpos=(i,j) tuple for goal coordinates (optional for part 1)
            stepnum int cut-off (optional for part 2)
    '''
    posnow = (1,1)
    if stepnum is None:
        mazelen = max(finalpos)*2
    else:
        mazelen = stepnum+1
    maze = get_maze(c,mazelen)

    paths = np.zeros((mazelen,mazelen),dtype=bool)
    paths[posnow] = True
    stepnow = 0
    while True:
        stepnow += 1
        paths = ndimage.binary_dilation(paths,mask=maze)
        if stepnum is not None:
            # part 2
            print('number of sites after {} steps: {}'.format(stepnow,paths.sum()))
            if stepnow==stepnum:
                break
        if finalpos is not None and paths[finalpos]:
            # part 1
            print('found first path with stepnum {}'.format(stepnow))
            return
        if paths[-1,:].any() or paths[:,-1].any():
            newmazelen = 2*mazelen
            maze = get_maze(c,newmazelen)
            newpaths = np.zeros((newmazelen,newmazelen),dtype=bool)
            newpaths[:mazelen,:mazelen] = paths
            mazelen,paths = newmazelen,newpaths
    print('done with steplen {}.'.format(paths.sum()))

    # plot maze
    imax = max(map(max,np.where(paths))) + 2
    print('\n'.join(map(''.join,np.where(maze[:imax,:imax],np.where(paths[:imax,:imax],'o',' '),'\033[1m#\033[0m'))))

def is_valid(x,y,c):
    if x>=0 and y>=0 and bin(int((x+y)**2+3*x+y+c)).count('1')%2==0:
        return True
    return False

def get_maze(c,mazelen):
    return np.vectorize(lambda x,y,c=c:is_valid(x,y,c),otypes=[bool])(*np.ogrid[:mazelen,:mazelen])


# more efficient alternative for part 1: A* search
# see A* wikipedia
def day13_part1_astar(c,finalpos=(31,39)):
    '''Inputs: int c primary input, finalpos=(i,j) tuple for goal coordinates'''
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
        relevant_scores = [fscore[pos] for pos in tovisit]
        minscore = min(relevant_scores)
        for posnow in tovisit:
            if fscore[posnow]==minscore:
                break
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
            tentative_gscore = gscore[posnow] + 1 #dist_between(current, neighbor)
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


if __name__=="__main__":
    # your c may vary
    c = 1364
    finalpos = (31,39)
    stepnum = 50
    print('part1:')
    #day13(c,finalpos=finalpos) # part 1 generic
    day13_part1_astar(c)       # part 1, more efficient than generic
    print('part2:')
    day13(c,stepnum=stepnum)   # part 2
