import numpy as np
from collections import deque

def day19(numelves):
    elves = np.arange(1,numelves+1)
    while elves.size>1:
        rollit = elves.size%2
        elves = elves[::2]
        if rollit:
            elves = np.roll(elves,1)
    print(elves[0])

def day19b(numelves):
    elves = deque(range(1,numelves+1))
    elves.rotate(-numelves//2+1)
    while numelves>1:
        elves.rotate(numelves%2-1)
        elves.popleft()
        numelves -= 1
    print(elves[0])

if __name__ == "__main__":
    numelves = 3014603 # may vary
    print('part1:')
    day19(numelves)
    print('part2:')
    day19b(numelves)
