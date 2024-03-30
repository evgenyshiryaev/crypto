# https://en.wikipedia.org/wiki/Linear_congruential_generator

import dataclasses
from gmpy2 import gcd, invert, is_prime
from sympy.ntheory import factorint


@dataclasses.dataclass
class Lcg:
    m: int
    a: int
    c: int
    x: int

    def next(self):
        self.x = (self.a * self.x + self.c) % self.m
        return self.x


# https://github.com/jvdsn/crypto-attacks/blob/master/attacks/lcg/parameter_recovery.py
def restore_params(y, m=None, a=None, c=None):
    if m is None:
        assert len(y) >= 4
        for i in range(len(y) - 3):
            d0 = y[i + 1] - y[i]
            d1 = y[i + 2] - y[i + 1]
            d2 = y[i + 3] - y[i + 2]
            g = d2 * d0 - d1 * d1
            m = g if m is None else gcd(g, m)

    if a is None:
        assert len(y) >= 3
        a = (y[2] - y[1]) * invert(y[1] - y[0], m) % m

    if c is None:
        assert len(y) >= 2
        c = (y[1] - a * y[0]) % m

    # verification
    lcg = Lcg(m, a, c, y[0])
    for i in range(1, len(y)):
        assert lcg.next() == y[i]

    return int(m), int(a), int(c)


if __name__ == '__main__':
    _m, _a, _c = 101, 53, 17
    _x = 69
    _lcg = Lcg(_m, _a, _c, _x)

    _y = [_lcg.next() for _ in range(6)]
    assert (_m, _a, _c) == restore_params(_y)

    _y = [_lcg.next() for _ in range(3)]
    assert (_m, _a, _c) == restore_params(_y, _m)

    _y = [_lcg.next() for _ in range(2)]
    assert (_m, _a, _c) == restore_params(_y, _m, _a)
