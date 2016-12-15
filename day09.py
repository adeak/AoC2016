import string
import re

def day9(inp):
    for ws in string.whitespace:
        inp = inp.replace(ws,'')
    out = ''
    while True:
        mark = re.search('\(\d+x\d+\)',inp)
        if not mark:
            break
        m,n = map(int,inp[mark.start()+1:mark.end()-1].split('x'))
        out += inp[:mark.start()] + n*inp[mark.end():mark.end()+m]
        inp = inp[mark.end()+m:]
    out += inp
    print(out)
    return len(out)


def day9b(inp):
    mark = re.search('\(\d+x\d+\)',inp)
    if not mark:
        return len(inp)
    m,n = map(int,inp[mark.start()+1:mark.end()-1].split('x'))
    return mark.start() + n*day9b(inp[mark.end():mark.end()+m]) + day9b(inp[mark.end()+m:])
