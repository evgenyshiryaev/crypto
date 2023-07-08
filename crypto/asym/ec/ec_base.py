# https://en.wikipedia.org/wiki/Elliptic_curve_point_multiplication
# https://cryptobook.nakov.com/asymmetric-key-ciphers/elliptic-curve-cryptography-ecc
# https://github.com/ashutosh1206/Crypton/tree/master/Elliptic-Curves

# 0 ≤ x, y < p

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
from nummaster.basic import sqrtmod
from typing import Iterator


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

    def __iter__(self) -> Iterator[int]:
        yield self.x
        yield self.y

    def __hash__(self):
        return hash((self.x, self.y))

    def to_bytes(self):
        l = len(hex(self.curve.p)[2:])
        return self.x.to_bytes(l, "big") + self.y.to_bytes(l, "big")

    def __neg__(self):
        return self.create(self.x, -self.y % self.curve.p)

    def __add__(self, Q):
        assert self.curve == Q.curve
        if isinstance(Q, Ideal):
            return self
        if self == -Q:
            return Ideal(self.curve)
        return self.add(Q)

    def __sub__(self, Q):
        return self + -Q

    def __mul__(self, n):
        if n < 0:
            return -self * -n
        R, Q = Ideal(self.curve), self
        while n:
            if n & 1:
                R += Q
            Q += Q
            n >>= 1
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

    def __hash__(self):
        return hash((self.x, self.y))

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


# utils

def compress_point(point):
    # another way - f'0{2 + y % 2}{hex(pubKey.x)[2:]}'
    return point[0], point[1] & 1


def uncompress_point(cpoint, p, a, b):
    x, is_odd = cpoint
    y = sqrtmod(pow(x, 3, p) + a * x + b, p)
    return (x, y) if bool(is_odd) == bool(y & 1) else (x, p - y)
