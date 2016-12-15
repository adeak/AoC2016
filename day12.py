def day12(inps,cstart):
    regs = {k:0 for k in list('abcd')}
    regs['c'] = cstart
    instrs = inps.strip().split('\n')
    i = 0
    while True:
        if i<0 or i==len(instrs):
            print(i,len(instrs))
            print(regs)
            print(regs['a'])
            return
        inst = instrs[i]
        #print(inst)
        tlist = inst.split(' ')
        if tlist[0]=='inc':
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
            regs[reg] = val
        else:
            print('weird input: {}'.format(inst))

        i += 1