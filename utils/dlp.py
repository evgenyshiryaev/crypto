# see sympy.ntheory.discrete_log()

import math
from sympy.ntheory import factorint, n_order
from utils.crt import crt


# https://en.wikipedia.org/wiki/Baby-step_giant-step
# a^x = b mod p
# n - order of a
# m = ceil(sqrt(n))
# i, j in [0, m)
# a^(im+j) = b
# a^j = b(a^-m)^i
# O(m) / O(m)
def bsgs(a, b, p, n=None):
    if n is None:
        n = n_order(a, p)
        # sage: Mod(a, p).multiplicative_order()
    m = math.ceil(math.sqrt(n))

    # baby step
    lookup = {}
    aj = 1
    for j in range(m):
        lookup[aj] = j
        aj = (aj * a) % p

    # giant step
    y = b
    am = pow(a, -m, p)
    for i in range(m):
        if y in lookup:
            return (i * m + lookup[y]) % p
        y = (y * am) % p
    return None


# https://en.wikipedia.org/wiki/Pohlig%E2%80%93Hellman_algorithm
# n = prod(pi^ei) - order of a
# O(sum(e*(log(order) + sqrt(p)))
def pohlig_hellman(a, b, p, n=None):
    if n is None:
        n = n_order(a, p)
    xs, ps = [], []
    for pi, ei in factorint(n).items():
        ni = pi ** ei
        ai, bi = pow(a, n // ni, p), pow(b, n // ni, p)
        xi = pohlig_hellman_prime(ai, bi, p, pi, ei)
        xs.append(xi)
        ps.append(ni)
    return crt(xs, ps)


def pohlig_hellman_prime(ai, bi, p, pi, ei):
    assert n_order(ai, p) == pi ** ei

    aik = pow(ai, pi ** (ei - 1), p)
    assert n_order(aik, p) == pi

    x = 0
    for k in range(ei):
        bik = pow(pow(ai, -x, p) * bi, pi ** (ei - 1 - k), p)
        xk = bsgs(aik, bik, p, pi)
        x += pi ** k * xk
    return x


if __name__ == '__main__':
    import random
    from sympy.ntheory import discrete_log, primitive_root

    _p = 604604729
    # _n = _p - 1 = 2^3 * 7^3 * 13 * 17 * 997
    _a = primitive_root(_p)  # 3
    _x = random.randrange(2, _p - 1)
    _b = pow(_a, _x, _p)
    assert _b == pow(_a, bsgs(_a, _b, _p), _p)
    assert _b == pow(_a, pohlig_hellman(_a, _b, _p), _p)
    assert _b == pow(_a, discrete_log(_p, _b, _a), _p)
