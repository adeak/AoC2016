from collections import defaultdict

def day20(inps,maxaddr=2**32-1):
    blocklims = defaultdict(lambda:0)
    blocklims[-1] = 0
    if type(inps)==str:
        inps = inps.split('\n')
    for inp in inps:
        bfrom,bto = map(int,inp.split('-'))
        blocklims[bfrom] += 1
        blocklims[bto] -= 1
    isblocked = 0
    allowedlist = []
    for lim in sorted(blocklims):
        isblocked += blocklims[lim]
        if isblocked==0 and blocklims[lim+1]==0 and lim+1<=maxaddr:
            allowedlist.append(lim+1)
            if len(allowedlist)==1:
                print('first allowed address: {}'.format(allowedlist[0]))
    print('number of allowed addresses: {}'.format(len(allowedlist)))


if __name__ == "__main__":
    inps = open('day20.inp','r').readlines()
    day20(inps)
