# https://github.com/ashutosh1206/Crypton/tree/master/RSA-encryption/Attack-LSBit-Oracle
# https://github.com/ashutosh1206/Crypton/tree/master/RSA-encryption/Attack-LSBit-Oracle-variant
# https://blog.bi0s.in/2019/09/29/Crypto/PubKey-Enc/InCTFi19-waRSAw/

import crypto.asym.rsa
import gmpy2
import random
import sympy
import tqdm


class LsbBinarySearch:
    def __init__(self, n, e, c):
        self.n = n
        self.e = e
        self.c = c

        self.left = sympy.Rational(0)  # or decimal
        self.right = sympy.Rational(n)
        self.i = 1

    def next_c(self):
        next_c = self.c * pow(2, self.i * self.e, self.n) % self.n
        self.i += 1
        return next_c

    def report_parity(self, bit):
        mid = (self.left + self.right) / 2
        if bit:
            self.left = mid
        else:
            self.right = mid


def hack_binary_search(m, n, e, d, c):
    hack = LsbBinarySearch(n, e, c)
    for _ in tqdm.tqdm(range(gmpy2.bit_length(n))):
        next_c = hack.next_c()
        hack.report_parity(pow(next_c, d, n) & 1)
    assert m == int(hack.right)


class LsbPlainTextBits:
    def __init__(self, n, e, c, m=0, i=0):
        self.n = n
        self.e = e
        self.c = c
        self.m = m
        self.i = i
        self.inv = gmpy2.invert(2, n)

    def next_c(self):
        return self.c * pow(self.inv, self.i * self.e, self.n) % self.n

    def report_parity(self, bit):
        bit = (bit - self.m * pow(self.inv, self.i) % self.n) & 1
        if bit:
            self.m |= (1 << self.i)
        self.i += 1


def hack_plain_text_bits(m, n, e, d, c):
    hack = LsbPlainTextBits(n, e, c)
    for _ in tqdm.tqdm(range(gmpy2.bit_length(n))):
        next_c = hack.next_c()
        hack.report_parity(pow(next_c, d, n) & 1)
    assert m == hack.m


def hack_plain_text_bits_restart(m, n, e, d, c):
    hack = LsbPlainTextBits(n, e, c)
    for i in tqdm.tqdm(range(gmpy2.bit_length(n) // 2)):
        next_c = hack.next_c()
        hack.report_parity(pow(next_c, d, n) & 1)
    hack = LsbPlainTextBits(n, e, c, hack.m, hack.i)
    for _ in tqdm.tqdm(range(i, gmpy2.bit_length(n))):
        next_c = hack.next_c()
        hack.report_parity(pow(next_c, d, n) & 1)
    assert m == hack.m


if __name__ == '__main__':
    _BITS = 128
    _e, _d, _n = crypto.asym.rsa.generate_key(_BITS)
    _m = random.randrange(1, _n)
    _c = pow(_m, _e, _n)

    hack_binary_search(_m, _n, _e, _d, _c)
    hack_plain_text_bits(_m, _n, _e, _d, _c)
    hack_plain_text_bits_restart(_m, _n, _e, _d, _c)
