def day23(inps,cstart=7):
    regs = {k:0 for k in list('abcd')}
    regs['a'] = cstart
    instrs = inps.strip().split('\n')
    i = 0
    trans = {'inc':'dec', 'dec':'inc', 'tgl':'inc', 'jnz':'cpy', 'cpy':'jnz'}
    while True:
        if i<0 or i==len(instrs):
            print(regs)
            print(regs['a'])
            return

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
        if tlist[0]=='tgl':
            reg = tlist[1]
            delta = regs[reg]
            if delta==0:
                i += 1
                continue
            if 0<=i+delta<len(instrs):
                tinst = instrs[i+delta].split()[0]
                instrs[i+delta] = instrs[i+delta].replace(tinst,trans[tinst])
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
    inps = open('day23.inp','r').read().strip()
    day23(inps,7)  # part 1
    day23(inps,12) # part 2
