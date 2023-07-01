from gmpy2 import invert


class LcgJava:
    m = 0xFFFFFFFFFFFF
    a = 25214903917
    c = 11

    def __init__(self, x0):
        self.x = x0

    def next(self):
        self.x = (self.a * self.x + self.c) & self.m
        print(self.x)
        return self.x >> 16

    def prev_seed_x(self, x0, x1):
        for i in range(0xFFFF + 1):
            seed = ((x0 << 16) + i)
            if ((self.a * seed + self.c) & self.m) >> 16 == x1:
                return seed
        return None

    def prev_seed(self, seed1):
        assert self.a & 1 == 1
        seed1 -= self.c
        seed0 = 0
        for i in range(48):
            mask = 1 << i
            bit = seed1 & mask
            seed0 |= bit
            if bit == mask:
                seed1 -= self.a << i
        return seed0

    def prev_seed_invert(self, seed1):
        seed0 = seed1 - self.c
        seed0 *= invert(self.a, self.m + 1)
        return seed0 & self.m


if __name__ == '__main__':
    _lcg_java = LcgJava(69)
    _x1 = _lcg_java.next()
    _x2 = _lcg_java.next()
    print(_x1, _x2)
    print(_lcg_java.prev_seed_x(_x1, _x2))
    print(_lcg_java.prev_seed(_lcg_java.x))
    print(_lcg_java.prev_seed_invert(_lcg_java.x))
