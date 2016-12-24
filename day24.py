import numpy as np
from scipy import ndimage
from itertools import permutations

def day24(inps):
    maze, coords = parse_maze(inps)
    nlen = coords.shape[1]
    dmat = -np.ones((nlen,nlen),dtype=np.int64) #-1 sentinel
    # build distance matrix
    for n in range(nlen):
        dmat = discover_pairs(n,maze,coords,dmat)

    # find shortest path
    dmat0 = dmat
    for part2 in False,True:
        dmat = np.array(dmat0)
        dist = np.inf
        for npath in permutations(range(1,nlen)):
            pfrom = np.append(0,npath[:-1])
            pto = npath
            if part2:
                pfrom = np.append(pfrom,npath[-1])
                pto = np.append(pto,0)
            dist = min(dist,dmat[pfrom,pto].sum())
        print('minimal path length: {}'.format(dist))



def parse_maze(inps):
    indat = np.array(list(map(list,inps.split('\n'))))
    maze = indat != '#'
    coords = np.where(maze & (indat!='.'))
    vals = indat[coords].astype(int)
    # sort values, although what matter is just that 0 comes first
    inds = np.argsort(vals)
    coords = np.array(coords)[:,inds] # (2*N) index array
    #print(vals)
    #print(coords)
    return maze,coords


def discover_pairs(n,maze,coords,dmat):
    posnow = coords[:,n]
    paths = np.zeros_like(maze).astype(bool)
    prevpaths = np.zeros_like(paths).astype(bool)
    paths[tuple(posnow)] = True
    stepnow = 0
    while True:
        stepnow += 1
        prevpaths[...] = paths
        paths = ndimage.binary_dilation(paths,mask=maze)
        newfound = paths[tuple(coords)] & ~prevpaths[tuple(coords)]
        newneighbs, = np.where(newfound)
        for nn in newneighbs:
            if dmat[n,nn] == -1:
                dmat[n,nn] = dmat[nn,n] = stepnow
            if np.sum(dmat[n,:] == -1)==1:
                # we're done
                return dmat

if __name__ == "__main__":
    inps = open('day24.inp','r').read().strip()
    day24(inps)
