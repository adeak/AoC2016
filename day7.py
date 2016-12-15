import re

def findpals(mystr,pallen):
    pals = []
    for k in range(len(mystr)-pallen+1):
        if pallen==4 and mystr[k]==mystr[k+3]!=mystr[k+2]==mystr[k+1]:
            pals.append(mystr[k:k+4])
        if pallen==3 and mystr[k]==mystr[k+2]!=mystr[k+1]:
            pals.append(''.join([mystr[k+1],mystr[k],mystr[k+1]]))
    return pals

def day7(inputs):
    goodTLS = 0
    goodSSL = 0
    for inp in inputs.split('\n'):
        parts = re.split('[\[\]]',inp)
        outs = '|||'.join(parts[::2])
        ins = '|||'.join(parts[1::2])
        outabbas = findpals(outs,4)
        inabbas = findpals(ins,4)
        babs = findpals(outs,3)
        if outabbas and not inabbas:
            goodTLS += 1
        if any(bab in ins for bab in babs):
            goodSSL += 1
    print(goodTLS,goodSSL)
