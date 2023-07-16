# see sympy.ntheory.nthroot_mod()

from gmpy2 import gcd

# p, q - primes
# g = gcd(p - 1, q - 1)
# a ^ ((p - 1) * (q - 1) / g) = 1 mod p * q


# p - prime
# gcd(e, p - 1) = 1
# x ^ e = c mod p
def n_root_p(e, c, p):
    f = p - 1
    assert gcd(e, f) == 1
    d = pow(e, -1, f)
    return pow(c, d, p)


# p, q - primes
# gcd(e, (p - 1) * (q - 1)) = 1
# x ^ e = c mod p * q
def n_root_pq(e, c, p, q):
    f = (p - 1) * (q - 1)
    assert gcd(e, f) == 1
    d = pow(e, -1, f)
    # or d = pow(e, -1, f // gcd(p - 1, q - 1))
    return pow(c, d, p * q)


if __name__ == '__main__':
    import sympy.ntheory

    _e, _c, _p = 1583, 4714, 7919
    _x = n_root_p(_e, _c, _p)
    assert pow(_x, _e, _p) == _c
    assert sympy.ntheory.is_nthpow_residue(_c, _e, _p)
    assert _x == sympy.ntheory.nthroot_mod(_c, _e, _p)

    _e, _c, _p, _q = 17389, 43927, 229, 281
    _x = n_root_pq(_e, _c, _p, _q)
    assert pow(_x, _e, _p * _q) == _c
    assert sympy.ntheory.is_nthpow_residue(_c, _e, _p * _q)
    assert _x == sympy.ntheory.nthroot_mod(_c, _e, _p * _q)[0]
