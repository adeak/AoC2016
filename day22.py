import numpy as np
from collections import defaultdict
from operator import itemgetter

def day22(inps):
    inps = inps.strip()
    for todel in r'/dev/grid/node-x',r'T',r'%':
        inps = inps.replace(todel,'')
    inps = inps.replace(r'-y',' ')
    inps = '\n'.join(inps.split('\n')[2:])
    alldat = np.fromstring(inps,sep=' ').reshape(-1,6).astype(np.int64)

    ylen,xlen = alldat[:,0:2].max(axis=0) + 1
    cells = np.empty((3,xlen,ylen),dtype=np.int64) # used/avail/size,x,y
    # watch out for stupid transposed definition...
    cells[0,alldat[:,1],alldat[:,0]] = alldat[:,3] # used
    cells[1,alldat[:,1],alldat[:,0]] = alldat[:,4] # avail
    cells[2,alldat[:,1],alldat[:,0]] = alldat[:,2] # size, relevant for part 2!

    # part 1:
    tcells = cells.reshape(cells.shape[0],-1) # flatten spatial grid
    viables = np.empty(xlen*ylen,dtype=np.int64)
    for ixy in range(xlen*ylen):
        tviables = (tcells[0,ixy]>0) & (tcells[0,ixy]<=tcells[1,:])
        tviables[ixy] = False
        viables[ixy] = tviables.sum()
    print('number of viable pairs: {}'.format(viables.sum())) # number of total pairs (part1 answer)

    # part 2: *few* assumptions
    # conjecture: there's always a single floating cell and a wall of blockers
    # conjecture: we can always move to neighbouring cell from posnow, at the cost of stepping there from the previous floater position
    cdot = '\N{middle dot}'
    printout = np.where(cells[0,...]>(cells[1,...].max()),'#',cdot) # start with '.'/'#' for non-/blocking cells
    printout[0,0] = 'x'  # exit
    printout[0,-1] = 'G' # goal
    printout[can_float(cells)] = 'o' # floater cells
    print('\n'.join(map(' '.join,printout)))
    print('"G" is target, "x" is exit, "o" can float, "#" is a blocking cell')

    # engage rock-solid assumptions
    blocking_x,blocking_y = np.where(cells[0,...]>(cells[1,...].max()))
    minblock,maxblock = [k(blocking_y) for k in (np.min,np.max)]
    floaters = np.where(can_float(cells))
    if floaters[0].size>1:
        print('ASSUMPTIONS FAILED: num_floaters=={} > 1'.format(floaters[0].size))
        return
    floater = [fl[0] for fl in floaters]
    evade_len_left = np.inf
    evade_len_right = np.inf
    if minblock!=0:
        evade_len_left = max(floater[1]-minblock+1,0) + (ylen-2)-(minblock-1)
    if maxblock!=ylen-1:
        evade_len_right = max(maxblock+1-floater[1],0) + max((ylen-2)-max(maxblock+1,floater[1]),0)
    evade_len = min(evade_len_left,evade_len_right)
    vertical_len = floater[0]
    circle_len = 5*(ylen-2-0)
    finalpush = 1
    print('Minimal length under working assumptions: {}'.format(evade_len + vertical_len + circle_len + finalpush))


def can_float(cells):
    xlen,ylen = cells.shape[1:]
    floatmask = np.empty((xlen,ylen),dtype=bool)
    for ix in range(xlen):
        if 0<ix<xlen-1:
            xneighbs = 2
        else:
            xneighbs = 1
        for iy in range(ylen):
            if 0<iy<ylen-1:
                yneighbs = 2
            else:
                yneighbs = 1
            floatmask[ix,iy] = len(list(getneighbs(ix,iy,cells)))==xneighbs+yneighbs
    if (~floatmask).all():
        print('ERROR: no floater found!')
    return floatmask


def getneighbs(x0,y0,cells):
    for xn,yn in (x0+1,y0),(x0-1,y0),(x0,y0+1),(x0,y0-1):
        if is_valid(xn,yn,x0,y0,cells):
            yield xn,yn

def is_valid(x,y,x0,y0,cells):
    if 0<=x<cells.shape[1] and 0<=y<cells.shape[2] and cells[1,x0,y0]>=cells[0,x,y]:
        return True
    return False


if __name__ == "__main__":
    inps = open('day22.inp','r').read()
    day22(inps)

