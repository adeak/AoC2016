from hashlib import md5

def day5(inp):
    if type(inp)==str:
        inp = bytes(inp,'ascii')
    code = []
    ind = 0
    while True:
        hexhash = md5(inp + str(ind).encode('ascii')).hexdigest()
        if hexhash.startswith('00000'):
            code.append(hexhash[5])
            print(hexhash[5])
        if len(code)==8:
            return ''.join(code)
        ind += 1


def day5b(inp):
    if type(inp)==str:
        inp = bytes(inp,'ascii')
    code = {}
    ind = 0
    while True:
        hexhash = md5(inp + str(ind).encode('ascii')).hexdigest()
        if hexhash.startswith('00000') and hexhash[5].isdigit() and int(hexhash[5]) in range(0,8) and hexhash[5] not in code:
            code[hexhash[5]] = hexhash[6]
            print(hexhash[6])
        if len(code)==8:
            return ''.join(list(zip(*sorted(code.items())))[1])
        ind += 1
