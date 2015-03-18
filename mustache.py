

def render(txt, var):
    return parse(txt, [var])

def parse(txt, var):
    stw = '{{'
    enw = '}}'
    cur = 0
    prs = False
    ret = ''
    mke = ''
    rtv = ''
    rtt = ''
    tmp = ''
    stk = 0

    for c in txt:
        # parsing code
        if prs:
            # instruction end
            if c == enw[cur]:
                cur += 1
                if cur == len(enw):
                    # variable and operator
                    if mke[:1] in ('#', '^', '/'):
                        ope = mke[:1]
                        mke = mke[1:]
                    else:
                        ope = ''
                    # search for value in multiple contexts
                    for ctx in var:
                        if ctx.__class__ == dict and mke in ctx:
                            val = ctx[mke]
                            break
                        else:
                            val = ''
                    # condition dependent
                    if rtv:
                        # closing previous
                        if ope == '/' and mke == rtv and stk == 1:
                            if prv == '#' and val:
                                if val.__class__ == list:
                                    for sub in val:
                                        ret += parse(rtt, [sub] + var)
                                else:
                                    ret += parse(rtt, [val] + var)
                            elif prv == '^' and not val:
                                ret += parse(rtt, var)
                            rtv = ''
                            rtt = ''
                        # another
                        else:
                            if mke == rtv:
                                if ope == '#':
                                    stk += 1
                                elif ope == '/':
                                    stk -= 1
                            rtt += stw + ope + mke + enw
                    else:
                        if ope:
                            prv = ope
                            rtv = mke
                            stk += 1
                        else:
                            if mke == '.':
                                ret += str(var[0])
                            else:
                                ret += str(val)
                    prs = False
                    cur = 0
                    mke = ''
                continue
            else:
                cur = 0
            
            # skip these chars
            if c in ('\t', ' '):
                continue

            # instruction
            mke += c
        # text
        else:
            if c == stw[cur]:
                cur += 1
                if cur == len(stw):
                    prs = True
                    cur = 0
                    tmp = ''
                    continue
                else:
                    tmp += c
            else:
                if tmp:
                    c = tmp + c
                    tmp = ''
                cur = 0
                if rtv:
                    rtt += c
                else:
                    ret += c
    
    return ret
