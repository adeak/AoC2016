from collections import deque
from hashlib import md5
import re

def hash_gen(inp,stretch=False):
    code = 0
    while True:
        out = md5(inp+str(code).encode('ascii')).hexdigest()
        if stretch:
            for _ in range(2016):
                out = md5(out.encode('ascii')).hexdigest()
        yield out
        code += 1

def day14(inp,stretch=False):
    if type(inp)==str:
        inp = bytes(inp,'ascii')
    hashgen = hash_gen(inp,stretch)
    queue = deque([next(hashgen) for _ in range(1001)],1001)
    codes = []
    code = 0
    while len(codes)<64:
        hashnow = queue.popleft()
        mat = re.search(r'(.)\1\1',hashnow)
        if mat:
            char = mat.group()[0]
            if any(char*5 in hsh for hsh in queue):
                codes.append(code)
                print(code)
        code += 1
        queue.append(next(hashgen))
    print(codes)
    #return codes

