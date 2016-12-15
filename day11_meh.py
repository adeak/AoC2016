# this one runs in finite-but-too-much time
# part 1 input gives a broad upper bound quickly with no cutoff
# sufficiently smaller-than-upper-bound cutoff gives optimal answer in ~hours
#
# it's suboptimal in multiple places, but it'd need a full rewrite to get a scalable solution anyway

from collections import deque, defaultdict
from itertools import combinations
from copy import deepcopy
import re

def parse_inputs(inps):
    elems = {}
    floors = defaultdict(set)
    for ifloor,inp in enumerate(inps.split('\n')):
        for icomp,comppatt in enumerate(('\w+ generator','\w+\-compatible microchip')):
            for compstring in re.findall(comppatt,inp):
                elem = re.split('[ -]',compstring,maxsplit=1)[0]
                if elem not in elems:
                    elems[elem] = len(elems)
                ielem = elems[elem]
                floors[ifloor].add((ielem,2*icomp-1)) # 1 for microchip, -1 for generator
    return floors

def next_levels(levelnow):
    if levelnow==0:
        return [levelnow+1]
    if levelnow==3:
        return [levelnow-1]
    return [levelnow-1,levelnow+1]

def validate_level(items):
    for elem,comp in items:
        # invalid if there is a lone microchip *and* any generator on the level
        if comp==1 and (elem,-comp) not in items:
            # see if there are other generators on the floor
            if any(telem!=elem and tcomp==-1 for telem,tcomp in items):
                return False
    return True

def finalstate(floors):
    if any(len(floors[ifloor])>0 for ifloor in range(3)):
        return False
    return True

def day11(inps,cutoff=-1):
    minpath = 1e100 # initial estimate
    floors = parse_inputs(inps)
    backlog = deque()
    floornow = 0
    numsteps = 0
    history = [(numsteps,floornow,deepcopy(floors))]
    while True:
        # determine possible next steps
        # floor choice first, elevator choice later -> prioritize 2 up, 1 down h/t Antti
        for floornext in next_levels(floornow):
            elevlist = list(combinations(floors[floornow],1))+list(combinations(floors[floornow],2))
            if floornext==floornow-1:
                # append/pop from the right -> append deferred ones first
                elevlist = reversed(elevlist)
            for televator in elevlist:
                # don't put a microchip and another generator in the elevator
                if len(televator)==2 and televator[0][1]+televator[1][1]==0 and televator[0][0]!=televator[1][0]:
                    continue
                elevator = set(televator)
                if validate_level(floors[floornext].union(elevator)) and validate_level(floors[floornow].difference(elevator)):
                    tmpfloors = deepcopy(floors)
                    tmpfloors[floornext].update(elevator)
                    for elev in elevator:
                        tmpfloors[floornow].discard(elev)
                    for numst,floorn,hist in history:
                        # check if we've been there before on a shorter path
                        if floorn==floornext and numst<=numsteps+1 and hist==tmpfloors:
                            break
                    else:
                        backlog.append((numsteps+1,floornext,tmpfloors))

        # now backlog contains all unvisited future paths
        while True:
            if len(backlog)==0:
                # out of future paths, we're done
                print('{} with cutoff {}'.format(minpath,cutoff))
                return
            numsteps,floornow,floors = backlog.pop()
            if numsteps==minpath:
                # no need to go on with this path
                continue
            if finalstate(floors):
                print('finalstate: {}'.format(floors))
                print('found a final state, numsteps={}'.format(numsteps))
                minpath = min(minpath,numsteps)
                continue
            if numsteps==cutoff:
                # next step would bee too long, don't go on with this path
                continue
            break
        # if we're here: we're on a possible path without an end so far --> continue
        history.append((numsteps,floornow,deepcopy(floors)))