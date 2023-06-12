# https://en.wikipedia.org/wiki/Baby-step_giant-step
# https://e-maxx.ru/algo/discrete_log
# https://en.wikipedia.org/wiki/Pohlig%E2%80%93Hellman_algorithm

import gmpy2
import math
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
def pohlig_hellman(a, b, n, factorization):
    xs, ps = [], []
    # factorization of (n-1)
    for p, e in factorization:
        pe = p ** e
        npe = (n - 1) // pe
        ai, bi = pow(a, npe, n), pow(b, npe, n)
        xi = bsgs(ai, bi, n)
        xs.append(xi)
        ps.append(pe)
    return crt(xs, ps)


if __name__ == '__main__':
    import random
    _a, _n = 7894352216, 604604729
    _x = random.randrange(2, _n - 1)
    _b = pow(_a, _x, _n)
    assert _b == pow(_a, bsgs(_a, _b, _n), _n)
    assert _b == pow(_a, pohlig_hellman(_a, _b, _n, ((2, 3), (7, 3), (13, 1), (17, 1), (997, 1))), _n)
