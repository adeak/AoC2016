import numpy as np
from itertools import permutations

def day21(inps,code='abcdefgh'):
    code = np.array(list(code))
    for inp in inps.split('\n'):
        if inp.startswith('swap position'):
            i1,i2 = map(int,(inp[14],inp[-1]))
            code[i1],code[i2] = code[i2],code[i1]
        elif inp.startswith('swap letter'):
            c1,c2 = inp[12],inp[-1]
            i1 = code==c1
            i2 = code==c2
            code[i1],code[i2] = code[i2],code[i1]
        elif inp.startswith('rotate left'):
            rot = int(inp.split(' ')[2])
            code = np.roll(code,-rot)
        elif inp.startswith('rotate right'):
            rot = int(inp.split(' ')[2])
            code = np.roll(code,rot)
        elif inp.startswith('rotate based on pos'):
            c = inp[-1]
            i = np.where(code==c)[0][0]
            numroll = i + 1 + (i>3)
            code = np.roll(code,numroll)
        elif inp.startswith('reverse positions'):
            words = inp.split(' ')
            i1,i2 = sorted(map(int,(words[2],words[-1])))
            code[i1:i2+1] = code[i1:i2+1][::-1]
        elif inp.startswith('move position'):
            words = inp.split(' ')
            i1,i2 = map(int,(words[2],words[-1]))
            if i1<i2:
                code[i1:i2+1] = np.append(code[i1+1:i2+1],code[i1])
            else:
                code[i2:i1+1] = np.append(code[i1],code[i2:i1])
        else:
            print('UNKNOWN LINE: {}'.format(inp))

    return ''.join(code)
                
def day21b(inps,code0='abcdefgh'):
    # brute force check for now; too lazy to refactor day21() to be invertable
    for code in permutations(code0):
        if day21(inps,''.join(code))==code0:
            return ''.join(code)

if __name__ == "__main__":
    inps = open('day21.inp','r').read().strip() # input commands
    # part1:
    print(day21(inps))
    # part 2: (brute force is fun!)
    code0 = 'fbgdceah' # may vary
    print(day21b(inps,code0))
