from Crypto.Random.random import getrandbits
from Crypto.Util.number import getPrime
import gmpy2
from utils.crt import crt


def generate_key(bits, e):
    while True:
        p, q = getPrime(bits), getPrime(bits)
        n = p * q
        f = (p - 1) * (q - 1)
        if e < f and gmpy2.gcd(e, f) == 1:
            return n


def hack(e, cs, ns):
    m = crt(cs, ns)
    gmpy2.get_context().precision = gmpy2.bit_length(m)
    return int(gmpy2.root(m, e))


if __name__ == '__main__':
    _BITS = 256

    _e = 11
    _ns = [generate_key(_BITS, _e) for _ in range(_e)]
    _m = getrandbits(_BITS)
    _cs = [pow(_m, _e, _n) for _n in _ns]
    _m_hacked = hack(_e, _cs, _ns)
    assert _m == _m_hacked
