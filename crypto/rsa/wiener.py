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

    return e, n


def hack(e, n):
    nd = utils.continued_fraction.from_cf(utils.continued_fraction.to_cf(e, n))
    for k, d in zip(nd[0], nd[1]):
        if k == 0:
            continue
        f = (e * d - 1) // k

        p = sympy.Symbol('p', integer=True)
        roots = sympy.solve(p ** 2 + (f - n - 1) * p + n, p)
        if len(roots) == 2 and roots[0] * roots[1] == n:
            return roots
    return None


if __name__ == '__main__':
    _BITS = 256

    _e, _n = generate_key(_BITS)
    ps = hack(_e, _n)
    assert ps is not None and ps[0] * ps[1] == _n
