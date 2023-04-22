# https://www.alpertron.com.ar/ECM.HTM

# https://github.com/RsaCtfTool/RsaCtfTool
# ./RsaCtfTool.py --createpub -n n -e e > key.pub
# ./RsaCtfTool.py --publickey key.pub --private --dump


from Crypto.Util.number import getPrime
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


if __name__ == '__main__':
    BITS = 256

    _p = getPrime(10)
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
