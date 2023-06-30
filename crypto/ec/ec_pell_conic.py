# Franz Lemmermeyer - Intruduction to Cryptography 2006

# x^2 - dy^2 = 1
# d != x^2 mod p
# (x0, y0) x (x1, y1) = (x0x1 + dy0y1, x0y1+x1y0)

from crypto.ec.ec_base import Curve, Ideal, Point
import dataclasses
from gmpy2 import legendre
from sympy.ntheory import sqrt_mod


@dataclasses.dataclass
class PellConic(Curve):
    d: int

    def order(self):
        return self.p - legendre(self.d, self.p)


@dataclasses.dataclass(eq=False)
class PellConicPoint(Point):
    def create(self, x, y):
        return PellConicPoint(self.curve, x, y)

    def add(self, Q):
        x = (self.x * Q.x + self.curve.d * self.y * Q.y) % self.curve.p
        y = (self.x * Q.y + self.y * Q.x) % self.curve.p
        return self.create(x, y)


# maps the pell conic to GF(p)ˆ* if d is square mod p
# https://arxiv.org/abs/2203.05290, section 3.2
class CurveFieldMap:
    def __init__(self, curve):
        assert legendre(curve.d, curve.p) == 1
        self.curve = curve
        self.s = sqrt_mod(curve.d, curve.p)

    def point_to_field(self, P):
        return (P.x - self.s * P.y) % self.curve.p

    def field_to_point(self, u):
        p = self.curve.p
        x = (1 + u ** 2) * pow(2 * u, p - 2, p) % p
        y = (1 - u ** 2) * pow(2 * self.s * u, p - 2, p) % p
        return PellConicPoint(self.curve, x, y)


if __name__ == '__main__':
    _curve = PellConic(7, -1)
    _g = PellConicPoint(_curve, 2, 2)
    _k = 0
    while True:
        _k += 1
        _p = _g * _k
        assert _p == _g.montgomery_ladder(_k)
        if _p == Ideal(_curve):
            break
    assert _k == _curve.order()


    _curve = PellConic(0x34096DC6CE88B7D7CB09DE1FEC1EDF9B448D4BE9E341A9F6DC696EF4E4E213B3, 3)
    _G = PellConicPoint(_curve, 2, 1)
    _P = PellConicPoint(_curve, 0x2FE4D1B7BA0F64D6E5BD5E4E8D55E898FF13B76974646D97BFDCD9DC688C0E2F, 0x8C33E2FC2957EFF24DD1CD5382169C3BFAAC2E75A900D322A8C84D3C641A27E)

    _field_map = CurveFieldMap(_curve)
    _g = _field_map.point_to_field(_G)
    _p = _field_map.point_to_field(_P)
