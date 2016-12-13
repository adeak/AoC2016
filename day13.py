import numpy as np
from collections import defaultdict
from operator import itemgetter
from scipy import ndimage

def is_valid(x,y,c):
    if x>=0 and y>=0 and bin(int((x+y)**2+3*x+y+c)).count('1')%2==0:
        return True
    return False

def get_maze(c,mazelen):
    return np.vectorize(lambda x,y,c=c:is_valid(x,y,c),otypes=[bool])(*np.ogrid[:mazelen,:mazelen])

def day13(c,finalpos=None,stepnum=None):
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
 
