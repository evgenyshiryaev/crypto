# https://en.wikipedia.org/wiki/Continued_fraction

# n - nominators
# d - denominators


def to_cf(n, d):
    q, r = n // d, n % d
    e = [q]
    while r:
        n, d = d, r
        q, r = n // d, n % d
        e.append(q)
    return e


def from_cf(e):
    n, d = [], []

    for i in range(len(e)):
        if i == 0:
            ni = e[i]
            di = 1
        elif i == 1:
            ni = e[i] * e[i-1] + 1
            di = e[i]
        else:
            ni = e[i] * n[i-1] + n[i-2]
            di = e[i] * d[i-1] + d[i-2]
        n.append(ni)
        d.append(di)

    return n, d


if __name__ == '__main__':
    _n = 11
    _d = 17
    _cf = to_cf(_n, _d)
    _ns, _ds = from_cf(_cf)
    assert (_n, _d) == (_ns[-1], _ds[-1])
