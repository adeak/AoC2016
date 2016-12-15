import numpy as np

def day8(inputs):
    disp = np.zeros((6,50),dtype=bool)
    for inp in inputs.split('\n'):
        if inp.startswith('rect'):
            A,B = map(int,inp.split(' ')[-1].split('x'))
            disp[:B,:A] = 1
        elif inp.startswith('rotate row y='):
            A,B = map(int,inp.split('=')[-1].split(' by '))
            disp[A,:] = np.roll(disp[A,:],B)
        elif inp.startswith('rotate column x='):
            A,B = map(int,inp.split('=')[-1].split(' by '))
            disp[:,A] = np.roll(disp[:,A],B)
    print(disp.sum())
    print('\n'.join(map(''.join,np.where(disp,' * ','   '))))
