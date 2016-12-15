mport re
from collections import Counter
    
def isreal(roomstr):
    for c in ['-','[',']']:
        roomstr = roomstr.replace(c,'') 
    name,id,checksum = re.match('([a-z]+)(\d+)([a-z]+)',roomstr).groups()
    freqs = Counter(name).most_common() # 5 here won't do
    freqs =sorted((-l,k) for k,l in freqs)
    newchecksum = ''.join(list(zip(*freqs))[1])[:5]
    return int(id) if checksum==newchecksum else 0


def day4(roomlist):
    return sum(map(isreal,roomlist.split('\n')))

###
    
def caesar(char,shift):
    if char==' ':
        return ' '
    for casefun in str.lower,str.upper:
        if casefun('a') <= char <= casefun('z'):
            return chr(ord(casefun('a')) + (ord(char) - ord(casefun('a')) + shift)%26)

def getrooms(roomlist):
    for roomstr in roomlist.split('\n'):
        if not isreal(roomstr):
            continue
        roomstr_t = roomstr.replace('-',' ')

        name,id,checksum = re.match('([a-zA-Z ]+)(\d+)(\[[a-zA-Z]+\])',roomstr_t).groups()
        yield ''.join(map(lambda char:caesar(char,int(id)),name)),id


def day4b(roomlist):
    parsed_dat = getrooms(roomlist)
    for name,id in parsed_dat:
        if 'pole' in name.lower() or 'object' in name.lower():
            print(name,id)
