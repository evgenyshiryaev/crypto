# by^2 = x^3 + ax^2 + x
# b * (a^2 - 4) = 0 - singular curve

from crypto.ec.ec_base import Curve, Ideal, Point
import dataclasses


@dataclasses.dataclass
class MontgomeryCurve(Curve):
    a: int
    b: int

    def is_singular(self):
        return self.b * (self.a**2 - 4) % self.p == 0


@dataclasses.dataclass(eq=False)
class MontgomeryPoint(Point):
    def create(self, x, y):
        return MontgomeryPoint(self.curve, x, y)

    def add(self, Q):
        if self == Q:
            m = (3 * self.x ** 2 + 2 * self.curve.a * self.x + 1) * pow(2 * self.curve.b * self.y, -1, self.curve.p)
        else:
            m = (Q.y - self.y) * pow(Q.x - self.x, -1, self.curve.p)
        x = (self.curve.b * m ** 2 - self.curve.a - self.x - Q.x) % self.curve.p
        y = (m * (self.x - x) - self.y) % self.curve.p
        return self.create(x, y)
