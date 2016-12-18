import numpy as np

def day18(inp,nrows=40,printtiles=False):
    '''Input: inp string of first row, nrows number of rows to check. Prints number of safe tiles.'''
    issafe = np.array(list(inp))=='.'
    safes = issafe.sum()
    if printtiles:
        print(np.where(issafe,'.','^'))
    for _ in range(nrows-1):
        padded = np.concatenate(([True],issafe,[True]))
        # trap if 2+1 or 1+2 pattern in previous row
        newtrap =(((padded[0:-2] == padded[1:-1]) & (padded[1:-1] != padded[2:])) |
                ((padded[0:-2] != padded[1:-1]) & (padded[1:-1] == padded[2:])))
        issafe = ~newtrap
        safes += issafe.sum()
        if printtiles:
            print(np.where(issafe,'.','^'))
    print(safes)


if __name__ == "__main__":
    inp = '.^..^....^....^^.^^.^.^^.^.....^.^..^...^^^^^^.^^^^.^.^^^^^^^.^^^^^..^.^^^.^^..^.^^.^....^.^...^^.^.'  # may vary
    # part 1-2
    for nrows in 40,400000:
        day18(inp,nrows=nrows)
