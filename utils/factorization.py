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


# n = (a - b) * (a + b)
# k * n + b^2 = a^2
def fact_squares_diff(n, m=100000):
    for k in (1, 3):
        kn = k * n
        for b in range(1, m):
            s = kn + b * b
            if gmpy2.is_square(s):
                a = int(gmpy2.sqrt(s))
                return int(gmpy2.gcd(a - b, n)), int(gmpy2.gcd(a + b, n))
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


def fact_pollard_p_1(n, m=100000):
    a = 2
    for j in range(2, m):
        a = pow(a, j, n)
        d = gmpy2.gcd(a - 1, n)
        if 1 < d < n:
            return d
    return None


# https://en.wikipedia.org/wiki/Shor%27s_algorithm
# a - fixed point, r - order
# a^r = 1 mod n
# n | a^r - 1
# n | (a^r/2 - 1) * (a^r/2 + 1)
def fact_shor(n, a, m=100000):
    for r in range(2, m, 2):
        if pow(a, r, n) == 1:
            break
    if r == m - 1:
        return None
    p = int(gmpy2.gcd(pow(a, r // 2, n) + 1, n))
    if p == 1 or p == n:
        return None
    return p, n // p


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

    assert (_p, _q) == fact_squares_diff(_p * _q)

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


    assert fact_pollard_p_1(13927189) == 3823
    assert fact_pollard_p_1(168441398857) == 350437
    _p, _q = getPrime(32), getPrime(32)
    assert fact_pollard_p_1(_p * _q) in (_p, _q)

    _n = 0x7fe8cafec59886e9318830f33747cafd200588406e7c42741859e15994ab62410438991ab5d9fc94f386219e3c27d6ffc73754f791e7b2c565611f8fe5054dd132b8c4f3eadcf1180cd8f2a3cc756b06996f2d5b67c390adcba9d444697b13d12b2badfc3c7d5459df16a047ca25f4d18570cd6fa727aed46394576cfdb56b41
    _a = 0x372f0e88f6f7189da7c06ed49e87e0664b988ecbee583586dfd1c6af99bf20345ae7442012c6807b3493d8936f5b48e553f614754deb3da6230fa1e16a8d5953a94c886699fc2bf409556264d5dced76a1780a90fd22f3701fdbcb183ddab4046affdc4dc6379090f79f4cd50673b24d0b08458cdbe509d60a4ad88a7b4e2921
    _p, _q = fact_shor(_n, _a)
    assert _n == _p * _q
