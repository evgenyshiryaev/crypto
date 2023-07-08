# https://github.com/ashutosh1206/Crypton/tree/master/RSA-encryption/Attack-Retrieve-Modulus

from Crypto.Util.number import getPrime
import gmpy2
import random


def generate_key(bits, e):
    while True:
        p, q = getPrime(bits), getPrime(bits)
        n = p * q
        f = (p - 1) * (q - 1)
        if e < f and gmpy2.gcd(e, f) == 1:
            break
    d = int(gmpy2.invert(e, f))
    return d, n


# c = pow(m, e, n)
# c - m**e = k*n
# n = gcd(c0 - m0**e, ..., ci - mi**e)
def hack_with_e(e, enc):
    n = None
    rounds = 5
    for _ in range(rounds):
        m = random.getrandbits(_BITS)
        c = enc(m)
        v = c - pow(m, e)
        n = gmpy2.gcd(n, v) if n is not None else v
    return n


# c = pow(m, e, n)
# c = m**e + k*n
# c**x = (m**x)**e + k*n
# n = gcd(c - c**x, ...)
def hack_without_e_pow(enc):
    n = None
    rounds = 5
    for _ in range(rounds):
        m = random.getrandbits(_BITS // 2)
        c0 = enc(m)
        c1 = enc(m * m)
        v = c0 * c0 - c1
        n = gmpy2.gcd(n, v) if n is not None else v
    return n


def hack_without_e_mul(enc):
    n = None
    rounds = 5
    for _ in range(rounds):
        m0 = random.getrandbits(_BITS // 2)
        m1 = random.getrandbits(_BITS // 2)
        m2 = m0 * m1
        c0, c1, c2 = enc(m0), enc(m1), enc(m2)
        v = c0 * c1 - c2
        n = gmpy2.gcd(n, v) if n is not None else v
    return n


if __name__ == '__main__':
    _BITS = 128
    _e = 17
    _d, _n = generate_key(_BITS, _e)

    assert _n == hack_with_e(_e, lambda m: pow(m, _e, _n))
    assert _n == hack_without_e_pow(lambda m: pow(m, _e, _n))
    assert _n == hack_without_e_mul(lambda m: pow(m, _e, _n))
