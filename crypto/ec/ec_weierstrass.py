# y^2 = x^3 + ax + b
# y^2 + a1xy + a3y = x^3 + a2x^2 + a4x + a6 - generalized Weierstrass

from crypto.ec.ec_base import Curve, Ideal, Point
import dataclasses


@dataclasses.dataclass
class WeierstrassCurve(Curve):
    a: int
    b: int

    def is_singular(self):
        return (4*self.a**3 + 27*self.b**2) % self.p == 0


@dataclasses.dataclass(eq=False)
class WeierstrassPoint(Point):
    def create(self, x, y):
        return WeierstrassPoint(self.curve, x, y)

    def add(self, Q):
        if self == Q:
            dydx = (3 * self.x**2 + self.curve.a) * pow(2 * self.y, -1, self.curve.p)
        else:
            dydx = (Q.y - self.y) * pow(Q.x - self.x, -1, self.curve.p)
        x = (dydx ** 2 - self.x - Q.x) % self.curve.p
        y = (dydx * (self.x - x) - self.y) % self.curve.p
        return self.create(x, y)


if __name__ == '__main__':
    _curve = WeierstrassCurve(17, 0, 7)
    _g = WeierstrassPoint(_curve, 15, 13)
    _k = 0
    while True:
        _k += 1
        _p = _g * _k
        assert _p == _g.montgomery_ladder(_k)
        if _p == Ideal(_curve):
            break
    assert _k == 18
