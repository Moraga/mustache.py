

def render(txt, var):
    stw = '{{'
    enw = '}}'
    cur = 0
    prs = False
    ret = ''
    mke = ''
    rtv = ''
    rtt = ''
    tmp = ''

    for c in txt:
        ## parsing
        if prs:
            ## instruction end
            if c == enw[cur]:
                cur += 1
                if cur == len(enw):
                    if rtv:
                        if mke[:1] == '/' and mke[1:] == rtv:
                            if ope == '#' and rtv in var and var[rtv]:
                                if var[rtv].__class__ == list:
                                    for sub in var[rtv]:
                                        ret += render(rtt, sub)
                                else:
                                    ret += render(rtt, var[rtv])
                            elif ope == '^' and (not rtv in var or not var[rtv]):
                                ret += render(rtt, var)
                            rtv = ''
                            rtt = ''
                        else:
                            rtt += stw + mke + enw
                    else:
                        if mke[:1] in ('#', '^'):
                            ope = mke[:1]
                            rtv = mke[1:]
                        else:
                            if mke == '.':
                                ret += var
                            elif mke in var:
                                ret += var[mke]
                    prs = False
                    cur = 0
                    mke = ''
                continue
            else:
                cur = 0
            
            ## skip chars
            if c in ('\t', ' '):
                continue

            ## instrution
            mke += c
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
