# https://en.wikipedia.org/wiki/Baby-step_giant-step
# https://e-maxx.ru/algo/discrete_log
# https://en.wikipedia.org/wiki/Pohlig%E2%80%93Hellman_algorithm
# see sympy.ntheory.discrete_log()

import gmpy2
import math
from sympy.ntheory import factorint
from utils.crt import crt


# a^x = b mod n
# n - order, gcd(a, n) = 1

# m = ceil(sqrt(n))
# i, j in [0, m)
# a^(im+j) = b
# a^j = b(a^-m)^i
# O(m)
def bsgs(a, b, n):
    assert gmpy2.gcd(a, n) == 1  # to calculate invert

    m = math.ceil(math.sqrt(n))

    # baby step
    lookup = {}
    aj = 1
    for j in range(m):
        lookup[aj] = j
        aj = (aj * a) % n

    # giant step
    y = b
    am = pow(a, -m, n)
    for i in range(m):
        if y in lookup:
            return (i * m + lookup[y]) % n
        y = (y * am) % n
    return None


# order = n - 1
# order = mult(p^e)
# O(sum(e*(log(order) + sqrt(p)))
def pohlig_hellman(a, b, p):
    n = p - 1  # order
    xs, ps = [], []
    for n0, n1 in factorint(n).items():
        ni = n0 ** n1
        ai, bi = pow(a, n // ni, p), pow(b, n // ni, p)
        xi = bsgs(ai, bi, p)
        xs.append(xi)
        ps.append(ni)
    return crt(xs, ps)


if __name__ == '__main__':
    import random
    from sympy.ntheory import discrete_log

    _a, _p = 7894352216, 604604729
    _x = random.randrange(1, _p)
    _b = pow(_a, _x, _p)
    assert _b == pow(_a, bsgs(_a, _b, _p), _p)
    assert _b == pow(_a, pohlig_hellman(_a, _b, _p), _p)
    assert _b == pow(_a, discrete_log(_p, _b, _a), _p)
