# https://www.alpertron.com.ar/ECM.HTM
# http://factordb.com/

# p, q - primes
# n = p * q
# f = (p - 1) * (q - 1)
# d = pow(e, -1, f), gcd(e, f) = 1


import gmpy2
from sympy import symbols, solve


def fact_small_p(n, m=100000):
    if n % 2 == 0:
        return 2, n // 2
    for p in range(3, m + 1, 2):
        if n % p == 0:
            return p, n // p
    return None


def fact_small_pq_diff(n, m=100000):
    gmpy2.get_context().precision = gmpy2.bit_length(n)
    n_sqrt = int(gmpy2.sqrt(n))
    for p in range(n_sqrt - m, n_sqrt):
        if n % p == 0:
            return p, n // p
    return None


def fact_same_p(n0, n1):
    gcd = int(gmpy2.gcd(n0, n1))
    return gcd, n0 // gcd, n1 // gcd if gcd != 1 else None


def fact_get_f(n, e, d):
    # e * d = 1 + k * f
    # f ~ n
    k = (e * d - 1) // n
    while True:
        f = (e * d - 1) // k
        if e * d - 1 == f * k:
            break
        k += 1
    return f


# f = (p - 1) * (q - 1) = n - (p + q) + 1
# x^2 - (p + q) * x + p * q = 0  - to solve
# (x - p) * (x - q) = 0
def fact_n_f(n, f):
    x = symbols('x')
    p_q = n + 1 - f
    p, q = solve(x * x + p_q * x + n)
    return -p, -q


if __name__ == '__main__':
    from Crypto.Util.number import getPrime, getRandomNBitInteger

    _BITS = 256

    _p, _q = getPrime(8), getPrime(_BITS)
    assert (_p, _q) == fact_small_p(_p * _q)

    _p = getPrime(_BITS)
    for _q in range(_p + 100000, _p + 1000000):
        if gmpy2.is_prime(_q):
            break
    assert (_p, _q) == fact_small_pq_diff(_p * _q)

    _p, _q0, _q1 = getPrime(_BITS), getPrime(_BITS), getPrime(_BITS)
    assert (_p, _q0, _q1) == fact_same_p(_p * _q0, _p * _q1)

    _p, _q = getPrime(_BITS), getPrime(_BITS)
    _n, _f = _p * _q, (_p - 1) * (_q - 1)
    while True:
        _e = getRandomNBitInteger(_BITS)
        if _e < _f and gmpy2.gcd(_e, _f) == 1:
            break
    _d = pow(_e, -1, _f)
    assert fact_get_f(_n, _e, _d) == _f

    _p, _q = getPrime(_BITS), getPrime(_BITS)
    _n, _f = _p * _q, (_p - 1) * (_q - 1)
    assert set([_p, _q]) == set(fact_n_f(_n, _f))
