import numpy as np

def day1(lststr):
    lst = lststr.split(', ')
    dirnow = 0
    posnow = [0,0]
    for k in lst:
        dirletter,num = k[0],int(k[1:])
        if dirletter=='R':
            dirnow -= np.pi/2
        else:
            dirnow += np.pi/2
        posnow = [posnow[0]+num*np.cos(dirnow), posnow[1]+num*np.sin(dirnow)]
    print(np.abs(posnow).sum())


def day1b(lststr):
    lst = lststr.split(', ')
    dirnow = 0
    posnow = [0,0]
    allpos = [posnow]
    for k in lst:
        dirletter,num = k[0],int(k[1:])
        if dirletter=='R':
            dirnow -= np.pi/2
        else:
            dirnow += np.pi/2
        for l in range(num):
            posnow = [np.round(posnow[0]+np.cos(dirnow)), np.round(posnow[1]+np.sin(dirnow))]
            if posnow in allpos:
                print(np.abs(posnow).sum())
                return
            else:
                allpos.append(posnow)
    print('single find:',np.abs(posnow).sum())
