# https://www.alpertron.com.ar/ECM.HTM

# https://github.com/RsaCtfTool/RsaCtfTool
# ./RsaCtfTool.py --createpub -n n -e e > key.pub
# ./RsaCtfTool.py --publickey key.pub --private --dump


from Crypto.Random.random import getrandbits
from Crypto.Util.number import getPrime
import gmpy2
import utils.garner


def small_prime(n, m=10000000):
    if n % 2 == 0:
        return 2, n // 2
    for p in range(3, m + 1, 2):
        if n % p == 0:
            return p, n // p
    return None


def small_difference(n, m=100000):
    gmpy2.get_context().precision = gmpy2.bit_length(n)
    n_sqrt = int(gmpy2.sqrt(n))
    for p in range(n_sqrt - m, n_sqrt):
        if n % p == 0:
            return p, n // p
    return None


def same_p(n0, n1):
    gcd = int(gmpy2.gcd(n0, n1))
    return gcd, n0 // gcd, n1 // gcd if gcd != 1 else None


def hastad_broadcast_generate_key(bits, e):
    while True:
        p = getPrime(bits)
        q = getPrime(bits)
        n = p * q
        f = (p - 1) * (q - 1)
        if e < f and gmpy2.gcd(e, f) == 1:
            break
    return n


def hastad_broadcast(e, cs, ns):
    m = utils.garner.solve(cs, ns)
    gmpy2.get_context().precision = gmpy2.bit_length(m)
    return int(gmpy2.root(m, e))


if __name__ == '__main__':
    BITS = 1024

    _p = getPrime(20)
    _q = getPrime(BITS)
    _p_hacked, _q_hacked = small_prime(_p * _q)
    assert _p == _p_hacked and _q == _q_hacked

    _p = getPrime(BITS)
    for _q in range(_p + 100000, _p + 1000000):
        if gmpy2.is_prime(_q):
            break
    _p_hacked, _q_hacked = small_difference(_p * _q)
    assert _p == _p_hacked and _q == _q_hacked

    _p = getPrime(BITS)
    _q0 = getPrime(BITS)
    _q1 = getPrime(BITS)
    _p_hacked, _q0_hacked, _q1_hacked = same_p(_p * _q0, _p * _q1)
    assert _p == _p_hacked and _q0 == _q0_hacked and _q1 == _q1_hacked

    _e = 3
    _n0 = hastad_broadcast_generate_key(BITS, _e)
    _n1 = hastad_broadcast_generate_key(BITS, _e)
    _n2 = hastad_broadcast_generate_key(BITS, _e)
    _m = getrandbits(BITS)
    _c0 = pow(_m, _e, _n0)
    _c1 = pow(_m, _e, _n1)
    _c2 = pow(_m, _e, _n2)
    _m_hacked = hastad_broadcast(_e, (_c0, _c1, _c2), (_n0, _n1, _n2))
    assert _m == _m_hacked
