def day25(inps,agood=0,bufflen=10):
    while True:
        if generate_signal(inps,agood,bufflen):
            break
        agood += 1

def generate_signal(inps,astart=0,bufflen=10):
    outvals = []
    regs = {k:0 for k in list('abcd')}
    regs['a'] = astart
    instrs = inps.strip().split('\n')
    i = 0
    while True:
        if i<0 or i==len(instrs):
            return False

        # check multiplication short-circuit
        if instrs[i].startswith('cpy') and all(instr.startswith(patt) for instr,patt in zip(instrs[i+1:6],['inc','dec','jnz','dec','jnz'])):
            cpyfrom,cpyto = instrs[i].split()[1:]
            sumshort = sum_short(instrs[i+1:i+4]) # returns regfrom->regto or None
            mulshort = mul_short(instrs[i+4:i+6]) # returns reg or None
            if sumshort and mulshort:
                sumfrom,sumto = sumshort
                mulvar = mulshort

                if mulvar not in regs and mulvar==cpyfrom or sumfrom!=cpyto:
                    # play it safe, just do cpy (it's not simple multiplication), don't figure this out now
                    if cpyfrom in regs:
                        val = regs[cpyfrom]
                    else:
                        val = int(cpyfrom)
                    if reg in regs:
                        regs[reg] = val
                    i += 1
                else:
                    # proper multiplication: mulvar*(sumto+=cpyfrom)
                    if cpyfrom in regs:
                        val = regs[cpyfrom]
                    else:
                        val = int(cpyfrom)
                    reg = sumto
                    regs[reg] += regs[mulvar]*val
                    i += 6
                continue
        
        # check separate addition-short-circuit
        sumshort = sum_short(instrs[i:i+2])
        if sumshort:
            regfrom,regto = sumshort
            regs[regto],regs[regfrom] = regs[regto]+regs[regfrom],0
            i += 3
            continue
        
        inst = instrs[i]
        tlist = inst.split(' ')
        if tlist[0]=='out':
            reg = tlist[1]
            if reg in regs:
                val = regs[reg]
            else:
                val = int(reg)
            if not 0<=val<=1:
                return False
            outvals.append(val)
            if len(outvals) == bufflen:
                if ((all(outvals[::2]) and not any(outvals[1::2])) or
                    (all(outvals[1::2]) and not any(outvals[::2]))):
                        print('signal accepted with value {}: (bufflen {}) {}'.format(astart,bufflen,outvals))
                        return True
                return False
            i += 1
            continue
        elif tlist[0]=='inc':
            reg = tlist[1]
            regs[reg] += 1
        elif tlist[0]=='dec':
            reg = tlist[1]
            regs[reg] -= 1
        elif tlist[0]=='jnz':
            cond = tlist[1]
            delta = tlist[2]
            if cond in regs:
                cond = regs[cond]
            else:
                cond = int(cond)
            if delta in regs:
                delta = regs[delta]
            else:
                delta = int(delta)
            if cond!=0:
                i += delta
                continue
        elif tlist[0]=='cpy':
            val = tlist[1]
            reg = tlist[2]
            if val in regs:
                val = regs[val]
            else:
                val = int(val)
            if reg in regs:
                regs[reg] = val
        else:
            print('weird input: {}'.format(inst))

        i += 1


def sum_short(instrs):
    if instrs[0].startswith('inc') and instrs[1].startswith('dec') and instrs[2]=='jnz {} -2'.format(instrs[1][4]):
        regto = instrs[0][4]
        regfrom = instrs[2][4]
        return regfrom,regto
    return None # be explicit

def mul_short(instrs):
    if instrs[0].startswith('dec') and instrs[1]=='jnz {} -5'.format(instrs[0][4]):
        regto = instrs[0][4]
        regfrom = instrs[1][4]
        if regto==regfrom:
            return regfrom
    return None # be explicit


if __name__ == "__main__":
    inps = open('day25.inp','r').read().strip()
    day25(inps)
