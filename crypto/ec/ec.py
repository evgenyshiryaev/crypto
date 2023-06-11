# https://en.wikipedia.org/wiki/Elliptic_curve_point_multiplication
# https://cryptobook.nakov.com/asymmetric-key-ciphers/elliptic-curve-cryptography-ecc
# https://github.com/ashutosh1206/Crypton/tree/master/Elliptic-Curves

# 0 ≤ x, y < p

# y^2 = x^3 + ax + b - Weierstrass
# 4a^3 + 27b^2 = 0 - singular curve

# y^2 + a1xy + a3y = x^3 + a2x^2 + a4x + a6 - generalized Weierstrass

# by^2 = x^3 + ax^2 + x - Montgomery
# b * (a^2 - 4) = 0 - singular curve

# x^2 + y^2 = 1 + dx^2y^2 - Edwards

# n = h * r
# n - order of curve / entire group
# h - cofactor, number of cyclic subgroups / partitions
# r - order of each subgroup, can be different in n is not prime

# G - generator / base point
# all points = G * [0..r)
# 0 * G = r * G - infinity

# k - private key (integer)
# P = k * G - public key (point)

import dataclasses

import gmpy2
from nummaster.basic import sqrtmod
import random


@dataclasses.dataclass
class Curve:
    p: int


@dataclasses.dataclass(eq=False)
class Point(object):
    curve: Curve
    x: int
    y: int

    def __eq__(self, other) -> bool:
        return type(other) is not Ideal and (self.x, self.y) == (other.x, other.y)

    def __ne__(self, other) -> bool:
        return not (self == other)

    def __neg__(self):
        return self.create(self.x, (-self.y) % self.curve.p)

    def __sub__(self, Q):
        return self + -Q

    def __mul__(self, n):
        if n < 0:
            return -self * -n
        if n == 0:
            return Ideal(self.curve)

        Q = self
        R = self if n & 1 == 1 else Ideal(self.curve)

        i = 2
        while i <= n:
            Q += Q
            if n & i == i:
                R += Q
            i <<= 1
        return R

    def __rmul__(self, n):
        return self * n

    def montgomery_ladder(self, n):
        R0, R1 = Ideal(self.curve), self
        for b in bin(n)[2:]:
            if b == '0':
                R0, R1 = R0 + R0, R0 + R1
            else:
                R0, R1 = R0 + R1, R1 + R1
        return R0


class Ideal(Point):
    def __init__(self, curve):
        self.curve = curve
        self.x, self.y = -1, -1  # just for print

    def __neg__(self) -> "Ideal":
        return self

    def __add__(self, Q):
        assert self.curve == Q.curve
        return Q

    def __mul__(self, n) -> "Ideal":
        assert isinstance(n, int)
        return self

    def __eq__(self, other) -> bool:
        return type(other) is Ideal

    def __rmul__(self, n):
        return self * n


# y^2 = x^3 + ax + b
@dataclasses.dataclass
class WeierstrassCurve(Curve):
    a: int
    b: int


@dataclasses.dataclass(eq=False)
class WeierstrassPoint(Point):
    def create(self, x, y):
        return WeierstrassPoint(self.curve, x, y)

    def __add__(self, Q):
        assert self.curve == Q.curve
        if isinstance(Q, Ideal):
            return self
        if self == -Q:
            return Ideal(self.curve)

        if self == Q:
            dydx = (3 * self.x**2 + self.curve.a) * pow(2 * self.y, -1, self.curve.p)
        else:
            dydx = (Q.y - self.y) * pow(Q.x - self.x, -1, self.curve.p)
        x = (dydx ** 2 - self.x - Q.x) % self.curve.p
        y = (dydx * (self.x - x) - self.y) % self.curve.p
        return self.create(x, y)


# by^2 = x^3 + ax^2 + x
@dataclasses.dataclass
class MontgomeryCurve(Curve):
    a: int
    b: int


@dataclasses.dataclass(eq=False)
class MontgomeryPoint(Point):
    def create(self, x, y):
        return MontgomeryPoint(self.curve, x, y)

    def __add__(self, Q):
        assert self.curve == Q.curve
        if isinstance(Q, Ideal):
            return self
        if self == -Q:
            return Ideal(self.curve)

        if self == Q:
            m = (3 * self.x ** 2 + 2 * self.curve.a * self.x + 1) * pow(2 * self.curve.b * self.y, -1, self.curve.p)
        else:
            m = (Q.y - self.y) * pow(Q.x - self.x, -1, self.curve.p)
        x = (self.curve.b * m ** 2 - self.curve.a - self.x - Q.x) % self.curve.p
        y = (m * (self.x - x) - self.y) % self.curve.p
        return self.create(x, y)


# utils

def compress_point(point):
    # another way - f'0{2 + y % 2}{hex(pubKey.x)[2:]}'
    return point[0], point[1] & 1


def uncompress_point(cpoint, p, a, b):
    x, is_odd = cpoint
    y = sqrtmod(pow(x, 3, p) + a * x + b, p)
    return (x, y) if bool(is_odd) == bool(y & 1) else (x, p - y)


def is_singular(p, a, b):
    return (4*a*a*a + 27*b*b) % p == 0


def kem(a, b, p, n, gx, gy):
    curve = WeierstrassCurve(p, a, b)
    g = WeierstrassPoint(curve, gx, gy)
    d0, d1 = random.randrange(2, n - 1), random.randrange(2, n - 1)
    q0, q1 = g * d0, g * d1
    s0, s1 = q0 * d1, q1 * d0
    assert s0 == s1


if __name__ == '__main__':
    _curve = WeierstrassCurve(17, 0, 7)
    print(_curve)
    _g = WeierstrassPoint(_curve, 15, 13)
    _k = 0
    while True:
        _k += 1
        _p = _g * _k
        assert _p == _g.montgomery_ladder(_k)
        print(f'{_k} * G = {_p})')
        if _p == Ideal(_curve):
            break
    assert _k == 18

    kem(497, 1768, 9739, 9739, 1804, 5368)  # n is not real
