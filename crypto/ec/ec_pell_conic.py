# Franz Lemmermeyer - Intruduction to Cryptography 2006

# x^2 - dy^2 = 1
# d != x^2 mod p
# (x0, y0) x (x1, y1) = (x0x1 + dy0y1, x0y1+x1y0)

from crypto.ec.ec_base import Curve, Ideal, Point
import dataclasses
from utils.square_root import legendre


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
