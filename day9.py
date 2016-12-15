# sorry for the uglies
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
    for ws in string.whitespace:
        inp = inp.replace(ws,'')
    outlen = 0
    while True: #loop over string slices
        mark = re.search('\(\d+x\d+\)',inp)
        if not mark:
            outlen += len(inp)
            return outlen

        # strategy: pull strings that contain only marks that are all inside
        #           --> run recursive expansion for each, hope for the best
        m,n = map(int,inp[mark.start()+1:mark.end()-1].split('x'))
        outlen += mark.start()
        tmpstring = n*inp[mark.end():mark.end()+m]
        inp = inp[mark.end()+m:]
        while True: # loop over tmpstring and query additional string chunks as needed
            mark = re.search('\(\d+x\d+\)',tmpstring)
            if not mark:
                outlen += len(tmpstring)
                break
            m,n = map(int,tmpstring[mark.start()+1:mark.end()-1].split('x'))
            restlen = len(tmpstring[mark.end():])
            if restlen<m:
                tmpstring,inp = tmpstring+inp[:m-restlen],inp[m-restlen:]
                continue
            # now we have a chunk that contains every character needed for its first marker
            # attempt for speed-up: if every marker inside is satisfied, do full expand, hope for the best
            # (otherwise it will run forever)
            for tmark in re.finditer('\(\d+x\d+\)',tmpstring):
                tm,tn = map(int,tmpstring[tmark.start()+1:tmark.end()-1].split('x'))
                if tm>len(tmpstring[tmark.end():]):
                    break
            else:
                # every marker is happy, chunk self-contained
                # (or there are no markers left)
                newlen = full_expand(tmpstring)
                outlen += newlen
                break

            # if there were discrepancies: do a small step of expansion outside
            outlen += mark.start()
            tmpstring = n*tmpstring[mark.end():mark.end()+m] + tmpstring[mark.end()+m:]

def full_expand(inp):
    # much recursion, wow
    mark = re.search('\(\d+x\d+\)',inp)
    if not mark:
        return len(inp)
    m,n = map(int,inp[mark.start()+1:mark.end()-1].split('x'))
    return mark.start() + n*full_expand(inp[mark.end():mark.end()+m]) + full_expand(inp[mark.end()+m:])
