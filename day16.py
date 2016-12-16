import numpy as np
from collections import deque

def day16(inp,disklen):
    inp = list(map(int,inp))
    inplen = len(inp)
    notpni = [1-i for i in inp[::-1]]
    # number of code replications to take
    numsteps = np.ceil(np.log2((disklen+1)/((inplen+1)))).astype(int)
    # number of hashing steps to take for checksum
    hashiter = 0
    while disklen%2**(hashiter+1)==0:
        hashiter += 1
    # initialize the code generator
    gencode = codegen(inp,notpni,numsteps)
    codedata = (next(gencode) for _ in range(disklen))
    # successively recompute checksum
    for k in range(hashiter):
        codedata = hashcode(codedata)
    # codedata is now the final checksum, actually
    print(''.join(map(str,codedata)))

def codegen(inp,notpni,numsteps):
    # brute-force stored seps for now
    seps = []
    for step in range(numsteps+1):
        seps.append(0)
        seps.extend((1-k for k in seps[-2::-1]))
    dseps = deque(seps)
    while True:
        yield from inp
        yield dseps.popleft()
        yield from notpni
        yield dseps.popleft()

def hashcode(codedata):
    def newhash(codedata):
        while True:
            try:
                yield int(next(codedata)==next(codedata))
            except StopIteration:
                break
    return newhash(codedata)


if __name__=="__main__":
    inp = '11110010111001001' # may vary
    # part1:
    print('part1:')
    day16(inp,disklen=272)
    # part1:
    print('part2:')
    day16(inp,disklen=35651584)

