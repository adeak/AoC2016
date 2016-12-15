from hashlib import md5
import random
import time
import string

inputcode = 'ugkcyxxp' # hardwired

def day5b_funky(inp):
    if type(inp)==str:
        inp = bytes(inp,'ascii')
    code = {}
    ind = 0
    print('Initiating hacking...')
    while True:
        if ind%10000==0:
            funkyprint(code)
        hexhash = md5(inp + str(ind).encode('ascii')).hexdigest()
        if hexhash.startswith('00000') and hexhash[5].isdigit() and int(hexhash[5]) in range(0,8) and hexhash[5] not in code:
            code[hexhash[5]] = hexhash[6]
        if len(code)==8:
            funkyprint(code,True)
            endprint(code)
            return ''.join(list(zip(*sorted(code.items())))[1])
        ind += 1

#def funkyprint(code, done=False): #original
#    output = ''.join(code[str(k)] if str(k) in code else '{:x}'.format(random.choice(range(16))) for k in range(8))
#    print('\r' + output + ' Hacking progress [' + '*'*3*len(code) + ' '*3*(8-len(code)) + '] {:3.0f}%'.format(len(code)/8*100),end='')

def funkyprint(code, done = False): #upgrade by @poke
    output = ''.join(code[str(k)] if str(k) in code else '{:x}'.format(random.choice(range(16))) for k in range(8))
    if not done:
        for _ in range(random.randrange(2)):
            print('\r' + ''.join([random.choice(string.digits + string.ascii_letters + string.punctuation) for _ in range(random.randrange(40, 75))]).ljust(76))
    print('\r' + output + ' Hacking progress [' + '*'*3*len(code) + ' '*3*(8-len(code)) + '] {:3.0f}%'.format(len(code)/8*100),end='')


def endprint(code):
    endcode = ''.join(list(zip(*sorted(code.items())))[1])
    for k in range(20):
        if k%2:
            print('\r\033[1m' + endcode + '\033[0m',end='')
        else:
            print('\r' + endcode,end='')
        time.sleep(0.5)


try:
    day5b_funky(inputcode)
except KeyboardInterrupt:
    pass
finally:
    print('')
