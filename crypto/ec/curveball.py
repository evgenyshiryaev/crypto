# https://crypto.stackexchange.com/questions/83308/what-is-the-chainoffools-curveball-attack-on-ecdsa-on-windows-10-cryptoapi

from crypto.ec.ec import WeierstrassCurve, WeierstrassPoint
import gmpy2
import random


def get_public_key(p, n, a, b, gx, gy):
    curve = WeierstrassCurve(p, a, b)
    G = WeierstrassPoint(curve, gx, gy)
    d = random.randrange(2, n - 1)
    return G * d


def curveball_0(n, Q):
    # d1 - random, gcd(d1, n) = 1
    # Q = G1 * d1
    # G1 = Q * d1_inv
    while True:
        d1 = random.randrange(2, n - 1)
        if gmpy2.gcd(d1, n) == 1:
            G1 = Q * pow(d1, -1, n)
            return G1, d1


def curveball_1(n, Q):
    # Q = Q * (n + 1)
    return Q, n + 1


if __name__ == '__main__':
    _p = 721805191
    _n = 721809392
    _a = 2
    _b = 3
    _gx = 37639372
    _gy = 158704036
    _Q = get_public_key(_p, _n, _a, _b, _gx, _gy)

    _G1, _d1 = curveball_0(_n, _Q)
    assert _G1 * _d1 == _Q

    _G1, _d1 = curveball_1(_n, _Q)
    assert _G1 * _d1 == _Q
