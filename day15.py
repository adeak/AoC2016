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

def day15(inps,part2=False):
    discnums,discstart = parse_inputs(inps,part2)
    time = 0
    tdeltas = np.arange(1,discnums.size+1)
    while True:
        if all(np.mod(discstart+tdeltas+time,discnums)==0):
            break
        time += 1
    print(time)

