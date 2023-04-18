# https://en.wikipedia.org/wiki/Mersenne_Twister
# https://github.com/tliston/mt19937/blob/main/mt19937.py

import random
import time
from utils.bits import INT_MAX, unshift_right_xor, unshift_left_mask_xor


class Mt19937:
    w, n, m, r = 32, 624, 397, 31
    a = 0x9908b0df
    u, d = 11, INT_MAX
    s, b = 7, 0x9d2c5680
    t, c = 15, 0xefc60000
    l = 18
    f = 1812433253

    def __init__(self, seed):
        self.MT = [0] * self.n
        self.index = self.n
        self.lower_mask = (1 << self.r) - 1
        self.upper_mask = dword(~self.lower_mask)
        self.MT[0] = dword(seed)
        for i in range(1, self.n):
            self.MT[i] = dword((self.f * (self.MT[i - 1] ^ (self.MT[i - 1] >> (self.w - 2))) + i))

    def next(self):
        if self.index >= self.n:
            self.twist()
            self.index = 0
        y = self.MT[self.index]
        y = temper(y)
        self.index += 1
        return dword(y)

    def twist(self):
        for i in range(self.n):
            x = (self.MT[i] & self.upper_mask) + (self.MT[(i + 1) % self.n] & self.lower_mask)
            xA = x >> 1
            if x % 2 != 0:
                xA = xA ^ self.a
            self.MT[i] = self.MT[(i + self.m) % self.n] ^ xA


def dword(x):
    return x & INT_MAX


def temper(y):
    y = y ^ ((y >> Mt19937.u) & Mt19937.d)
    y = y ^ ((y << Mt19937.s) & Mt19937.b)
    y = y ^ ((y << Mt19937.t) & Mt19937.c)
    y = y ^ (y >> Mt19937.l)
    return y


def untemper(y):
    y = unshift_right_xor(y, Mt19937.l)
    y = unshift_left_mask_xor(y, Mt19937.t, Mt19937.c)
    y = unshift_left_mask_xor(y, Mt19937.s, Mt19937.b)
    y = unshift_right_xor(y, Mt19937.u)
    return y


if __name__ == '__main__':
    _rng = Mt19937(random.randrange(INT_MAX))
    print(_rng.next(), _rng.next())

    _rng_copy = Mt19937(0)  # any seed
    for _i in range(Mt19937.n):
        _rng_copy.MT[_i] = untemper(random.randrange(INT_MAX))
    for _ in range(Mt19937.n):
        assert random.randrange(INT_MAX) == _rng_copy.next()
