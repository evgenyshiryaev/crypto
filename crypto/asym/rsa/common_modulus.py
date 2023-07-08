# https://github.com/ashutosh1206/Crypton/tree/master/RSA-encryption/Attack-Common-Modulus

# !!! works only if pow(m, gcd(e0, e1)) < n !!!
# c0 = pow(m, e0, n)
# c1 = pow(m, e1, n)
# (e0 * a) + (e1 * b) = gcd(e0, e1)
# (pow(c0, a, n) * pow(c1, b, n)) % n = pow(m, gcd(e0, e1), n)

from Crypto.Util.number import bytes_to_long, getPrime, getRandomNBitInteger
import gmpy2


def hack(n, e0, e1, c0, c1):
    gcd, a, b = gmpy2.gcdext(e0, e1)
    c0a = pow(c0, a, n) if a >= 0 else pow(gmpy2.invert(c0, n), -a, n)
    c1a = pow(c1, b, n) if b >= 0 else pow(gmpy2.invert(c1, n), -b, n)
    return gmpy2.iroot((c0a * c1a) % n, gcd)


def generate_key(bits):
    p, q = getPrime(bits), getPrime(bits)
    n = p * q
    f = (p - 1) * (q - 1)
    while True:
        e0, e1 = getRandomNBitInteger(bits), getRandomNBitInteger(bits)
        if e0 < f and gmpy2.gcd(e0, f) == 1 and e1 < f and gmpy2.gcd(e1, f) == 1:
            break
    d0, d1 = int(gmpy2.invert(e0, f)), int(gmpy2.invert(e1, f))
    return e0, d0, e1, d1, n


if __name__ == '__main__':
    _BITS = 128
    _e0, _d0, _e1, _d1, _n = generate_key(_BITS)

    _m = bytes_to_long(b'Don\'t use common modulus')
    _c0, _c1 = pow(_m, _e0, _n), pow(_m, _e1, _n)

    _m_hacked, _is_root = hack(_n, _e0, _e1, _c0, _c1)
    assert _is_root  # in case pow(m, gcd(e0, e1)) >= n
    assert _m == _m_hacked
