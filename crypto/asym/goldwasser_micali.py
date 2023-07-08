# https://en.wikipedia.org/wiki/Goldwasser%E2%80%93Micali_cryptosystem

from Crypto.Util.number import bytes_to_long, getPrime, long_to_bytes
from gmpy2 import gcd, kronecker, legendre
from random import randrange


def generate_key(bits):
    p, q = getPrime(bits), getPrime(bits)
    n = p * q
    while True:
        x = randrange(2, n)
        if legendre(x, p) == -1 and legendre(x, q) == -1:
            assert kronecker(x, n) == 1
            return (x, n), (p, q)


def encrypt(m, pub_key):
    x, n = pub_key
    c = []
    for b in bin(bytes_to_long(m))[2:]:
        while True:
            y = randrange(2, n)
            if gcd(y, n) == 1:
                c.append(y**2 * x**int(b) % n)
                break
    return c


def decrypt(c, priv_key):
    p, q = priv_key
    m = ''.join(['0' if legendre(ci, p) == 1 and legendre(ci, q) == 1 else '1' for ci in c])
    return long_to_bytes(int(m, 2))


if __name__ == '__main__':
    _pub_key, _priv_key = generate_key(64)
    _m = b'soo unsecret'
    _c = encrypt(_m, _pub_key)
    assert _m == decrypt(_c, _priv_key)
