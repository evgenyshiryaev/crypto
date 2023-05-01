# https://www.alpertron.com.ar/ECM.HTM

# https://github.com/RsaCtfTool/RsaCtfTool
# ./RsaCtfTool.py --createpub -n n -e e > key.pub
# ./RsaCtfTool.py --publickey key.pub --private --dump


from Crypto.Util.number import getPrime, getRandomNBitInteger
import gmpy2


def small_prime(n, m=100000):
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


def get_f(n, e, d):
    # d = gmpy2.invert(e, f)
    # ed = 1 + kf
    # f ~ n
    k = (e * d - 1) // n
    while True:
        f = (e * d - 1) // k
        if e * d - 1 == f * k:
            break
        k += 1
    return f


if __name__ == '__main__':
    BITS = 256

    _p, _q = getPrime(10), getPrime(BITS)
    _p_hacked, _q_hacked = small_prime(_p * _q)
    assert _p == _p_hacked and _q == _q_hacked

    _p = getPrime(BITS)
    for _q in range(_p + 100000, _p + 1000000):
        if gmpy2.is_prime(_q):
            break
    _p_hacked, _q_hacked = small_difference(_p * _q)
    assert _p == _p_hacked and _q == _q_hacked

    _p, _q0, _q1 = getPrime(BITS), getPrime(BITS), getPrime(BITS)
    _p_hacked, _q0_hacked, _q1_hacked = same_p(_p * _q0, _p * _q1)
    assert _p == _p_hacked and _q0 == _q0_hacked and _q1 == _q1_hacked

    _p, _q = getPrime(BITS), getPrime(BITS)
    _n = _p * _q
    _f = (_p - 1) * (_q - 1)
    while True:
        _e = getRandomNBitInteger(BITS)
        if _e < _f and gmpy2.gcd(_e, _f) == 1:
            break
    _d = int(gmpy2.invert(_e, _f))
    _f_hacked = get_f(_n, _e, _d)
    assert _f == _f_hacked

