# https://sagi.io/2016/04/crypto-classics-wieners-rsa-attack/

from Crypto.Util.number import getPrime
import gmpy2
import utils.continued_fraction
import random
import sympy


def generate_key(bits):
    while True:
        p, q = getPrime(bits), getPrime(bits)
        if q < p < 2 * q:
            break
    n = p * q
    f = (p - 1) * (q - 1)

    max_d = gmpy2.isqrt(gmpy2.isqrt(n)) // 3
    while True:
        d = random.randrange(3, max_d)
        if gmpy2.gcd(d, f) == 1:
            break
    e = int(gmpy2.invert(d, f))

    return n, e, d


def hack(n, e):
    m = random.randrange(2, n)
    c = pow(m, e, n)
    nd = utils.continued_fraction.from_cf(utils.continued_fraction.to_cf(e, n))
    for k, d in zip(nd[0], nd[1]):
        if m != pow(c, d, n):
            continue
        f = (e * d - 1) // k
        p = sympy.Symbol('p', integer=True)
        roots = sympy.solve(p ** 2 + (f - n - 1) * p + n, p)
        return roots[0], roots[1], d
    return None


if __name__ == '__main__':
    _n, _e, _d = generate_key(256)
    _hacked = hack(_n, _e)
    assert (_n, _d) == (_hacked[0] * _hacked[1], _hacked[2])
