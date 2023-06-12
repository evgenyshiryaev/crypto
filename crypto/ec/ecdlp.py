# https://ru.wikipedia.org/wiki/ECDLP
# https://github.com/ashutosh1206/Crypton/tree/master/Discrete-Logarithm-Problem/Elliptic-Curve-DLP

from crypto.ec.ec import Ideal
import math
from utils.crt import crt

# P*d = Q
# n - order


# O(n)
def bruteforce(P, Q):
    T = P
    d = 1
    while True:
        if T == Q:
            return d
        T += P
        d += 1


# O(sqrt(n))
def bsgs(P, Q, n):
    m = math.ceil(math.sqrt(n))

    # baby step
    lookup = {}
    Pi = Ideal(P.curve)
    for i in range(m):
        lookup[Pi] = i
        Pi += P

    # giant step
    Qi = Q
    T = P * m
    for j in range(m):
        if Qi in lookup:
            return (j * m + lookup[Qi]) % n
        Qi -= T
    return None


# n = mult(p^e)
# O(sum(e*(log(order) + sqrt(p)))
def pohlig_hellman(P, Q, n, factorization):
    xs, ps = [], []
    # factorization of n
    for p, e in factorization:
        pe = p ** e
        npe = (n - 1) // pe
        Pi, Qi = P * npe, Q * npe
        xi = bsgs(Pi, Qi, n)
        xs.append(xi)
        ps.append(pe)
    return crt(xs, ps)


if __name__ == '__main__':
    from crypto.ec.ec import WeierstrassCurve, WeierstrassPoint
    import random

    _p = 721805191
    _n = 721809392
    _a = 2
    _b = 3
    _curve = WeierstrassCurve(_p, _a, _b)
    _P = WeierstrassPoint(_curve, 48863429, 33626183)
    _d = random.randrange(2, _n - 1)
    _Q = _P * _d

    # assert _d == bruteforce(_P, _Q)  # too slow
    assert _d == bsgs(_P, _Q, _n)
    # factorization is generated with sagemath's factor()
    assert _d == pohlig_hellman(_P, _Q, _n, ((2, 4), (17, 1), (19, 2), (7351, 1)))
