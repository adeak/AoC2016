from hashlib import md5
from operator import lt,gt

msize = 4

def day17(inp,pos0=(0,0),minfind=True):
    allpaths = recurse_search(inp,pos0,minfind)
    if not allpaths:
        print('No valid path found.')
        return
    if minfind:
        bestlen = float('inf')
        checkfun = lt
        print('Shortest path:')
    else:
        bestlen = -1
        checkfun = gt
        print('Longest path:')
    for path in allpaths:
        if checkfun(len(path),bestlen):
            bestpath = path
            bestlen = len(bestpath)
    #print(bestpath)
    print('path: {}'.format(bestpath[len(inp):]))
    print('length: {}'.format(len(bestpath[len(inp):])))
    

def opendoors_eh(path,pos):
    hashchars = md5(path.encode('ascii')).hexdigest()[:4]
    # order is up-down-left-right, returns boolean for being open
    opendoors = ['UDLR'[i] for i,n in enumerate(hashchars) if int(n,16)>10]
    forbid = []
    if pos[0] == 0:
        forbid.append('U')
    elif pos[0] == msize-1:
        forbid.append('D')
    if pos[1] == 0:
        forbid.append('L')
    elif pos[1] == msize-1:
        forbid.append('R')
    for f in forbid:
        try:
            opendoors.remove(f)
        except ValueError:
            pass
    return opendoors
        

def recurse_search(pathhere,posnow,minfind):
    nextdoors = opendoors_eh(pathhere,posnow)
    mypath = []
    for door in nextdoors:
        if door == 'U':
            newpos = posnow[0]-1,posnow[1]
        elif door == 'D':
            newpos = posnow[0]+1,posnow[1]
        elif door == 'L':
            newpos = posnow[0],posnow[1]-1
        else:
            newpos = posnow[0],posnow[1]+1
        newpath = pathhere + door
        if newpos == (3,3):
            if minfind:
                # no other door can lead here from this path, we're done now if shortest needed
                return [newpath]
            else:
                # need to check other, longer paths from here
                mypath.extend([newpath])
                continue
        restpaths = recurse_search(newpath,newpos,minfind)
        if restpaths:
            mypath.extend(restpaths)
    return mypath


if __name__ == "__main__":
    inp = 'udskfozm' # may vary
    # part 1:
    day17(inp,minfind=True)
    # part 2:
    day17(inp,minfind=False)
