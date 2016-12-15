import numpy as np

def parse_inputs(inps,part2):
    discnums = {}
    discstart = {}
    for inp in inps.split('\n'):
        tinp = inp[6:].split(' ')
        discnums[int(tinp[0])] = int(tinp[2])
        discstart[int(tinp[0])] = int(tinp[-1][:-1])
    if part2:
        newdisc = max(discnums)+1
        discnums[newdisc] = 11
        discstart[newdisc] = 0
    discnums = np.array([discnums[k] for k in sorted(discnums)])
    discstart = np.array([discstart[k] for k in sorted(discstart)])
    return discnums,discstart

def day15(inps,part2=False,blocksize=int(1e4)):
    discnums,discstart = parse_inputs(inps,part2)
    nblock = 0
    tdeltas = np.arange(1,discnums.size+1)
    timeblock = np.arange(0,blocksize)[:,None]
    while True:
        blockcheck = np.all(np.mod(discstart+tdeltas+timeblock+nblock*blocksize,discnums)==0,axis=1)
        if any(blockcheck):
            print(nblock*blocksize + np.where(blockcheck)[0][0])
            return
        nblock += 1

