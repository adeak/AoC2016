from collections import defaultdict

class Bot():
    def __init__(self,val=None,to=None):
        self.nums = set()
        self.to = {}
        if val is not None:
            self.nums.add(val)
        if to is not None:
            self.to.update(to)
    def instruct(self,to):
        self.to.update(to)
    def give(self,val):
        if val in self.nums or len(self.nums)==2:
            print(self.nums)
            raise Exception("Problem, shouldn't happen!")
        self.nums.add(val)
    def take(self):
        if len(self.nums)<2:
            return None
        tnums = list(self.nums)
        lowto,highto = self.to['low'],self.to['high']
        self.nums.clear()
        return ((min(tnums),lowto),(max(tnums),highto))

class Hive():
    def __init__(self,spec):
        self.bots = defaultdict(Bot)
        self.outs = defaultdict(list)
        self.special = spec

    def parse_inputs(self,inps):
        instructs = []
        rest = []
        for inp in inps.split('\n'):
            if inp.startswith('bot '):
                instructs.append(inp)
            else:
                rest.append(inp)
        self.parse_instructs(instructs)
        self.parse_rest(rest)

    def parse_instructs(self,inps):
        for inp in inps:
            if inp.startswith('value '):
                continue
            else:
                tinp = inp[4:].split(' gives low to ')
                ibot = int(tinp[0])
                lowinp,highinp = tinp[1].split(' and high to ')
                lowhigh = []
                for tinp in lowinp,highinp:
                    if tinp.startswith('output'):
                        lowhigh.append(-int(tinp[7:])-1)
                    else:
                        lowhigh.append(int(tinp[4:]))
                self.bots[ibot].instruct({'low':lowhigh[0], 'high':lowhigh[1]})

    def parse_rest(self,inps):
        for inp in inps:
            if not inp.startswith('value'):
                continue
            else:
                val,ibot = map(int,inp[6:].split(' goes to bot '))
                self.bots[ibot].give(val)
            while True:
                if not self.step_all():
                    break

    def step_all(self):
        didstuff = False
        for ibot,bot in self.bots.items():
            took = bot.take()
            if took:
                didstuff = True
                if {took[0][0],took[1][0]} == self.special:
                    print('bot {} compares numbers {} and {}.'.format(ibot,*self.special))
                for num,to in took:
                    if to<0:
                        self.outs[to].append(num)
                    else:
                        runagain = False
                        if to not in self.bots:
                            # new bot: need to rerun, iterator is corrupted
                            runagain = True
                        self.bots[to].give(num)
                        if runagain:
                            return True
        return didstuff

def day10(inps,spec,part2):
    # spec is a 2-element set that defines which bot to look for
    # part2 is a sequence of output bins, the values of which to multiply
    hive = Hive(spec)
    hive.parse_inputs(inps)
    while True:
        if not hive.step_all():
            prod = 1
            for outbin in part2:
                prod *= hive.outs[-outbin-1][0]
            print('product of output bins '+('{} '*len(part2)).format(*part2) +': {}'.format(prod))
            return
