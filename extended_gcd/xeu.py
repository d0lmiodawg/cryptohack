def xeu(r1, r2, q1=None, q2=None, p1=None, p2=None, n=None):
    if n is None:
        first = True
        n = r1
    else:
        first = False
    if p2 is None:
        p2 = 0
    elif p1 is None:
        p1 = 0
        p2 = 1
    else:
        p1, p2 = p2, (p1 - p2*q1) % n
        print(p1 - p2*q1)
    print(q1, q2, p1, p2)
    if r2 == 0:
        r, s = r1, p2
    else:
        r, s = xeu(r2, r1 % r2, q2, r1 // r2, p1, p2, n)
    if first:
        return r, s, (r-s*r2)//r1
    else:
        return r, s

print(xeu(32321, 26513))