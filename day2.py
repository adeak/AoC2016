import numpy as np

def day2(codestr):
    nums = np.arange(1,10).astype(np.int64).reshape(3,3)
    lastind = np.array([1,1])
    code = []
    for codeline in codestr.split('\n'):
        for lett in codeline:
            if lett=='U':
                delta = [-1,0]
            elif lett=='D':
                delta = [1,0]
            elif lett=='R':
                delta = [0,1]
            else:
                delta = [0,-1]
            lastind = np.clip(lastind+delta,0,2)
        code.append(str(nums[tuple(lastind)]))
    return ''.join(code)

def day2b(codestr):
    nums = np.array(list('0010002340567890ABC000D00')).reshape(5,5)
    lastind = np.array([2,0])
    code = []
    for codeline in codestr.split('\n'):
        for lett in codeline:
            if lett=='U':
                delta = [-1,0]
            elif lett=='D':
                delta = [1,0]
            elif lett=='R':
                delta = [0,1]
            else:
                delta = [0,-1]
            tmpind = np.clip(lastind+delta,0,4)
            if nums[tuple(tmpind)]!='0':
                lastind = tmpind
        code.append(nums[tuple(lastind)])
    return ''.join(code)
