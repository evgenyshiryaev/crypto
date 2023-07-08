# https://en.wikipedia.org/wiki/Quadratic_residue
# https://en.wikipedia.org/wiki/Quadratic_residuosity_problem
# see sympy.ntheory.sqrt_mod
# see nummaster.basic.sqrtmod

# r^2 = a mod p

# (a/p)
# p>2 - prime
# https://en.wikipedia.org/wiki/Legendre_symbol
# use gmpy2.legendre()
def legendre(a, p):
    if a % p == 0:
        return 0
    return 1 if pow(a, (p - 1) // 2, p) == 1 else -1


# (a/n) = (a/p0)^e0 * ... * (a/pk)^ek
# n = p0^e0 * ... * pk^ek, n>0 odd
# https://en.wikipedia.org/wiki/Jacobi_symbol
# use gmpy2.jacobi()


# https://en.wikipedia.org/wiki/Kronecker_symbol
# n - any
# use gmpy2.kronecker()


# p = 3 mod 4, p - prime
def sqrtmod_3_4(a, p):
    assert p % 4 == 3
    return min_root(pow(a, (p + 1) // 4, p), p)


# p = 5 mod 8, p - prime
def sqrtmod_5_8(a, p):
    assert p % 8 == 5
    v = pow(2 * a, (p - 5) // 8, p)
    i = (2 * a * v * v) % p
    return min_root((a * v * (i - 1)) % p, p)


def min_root(r, p):
    return min(r, -r % p)


if __name__ == '__main__':
    import sympy.ntheory
    import gmpy2

    _p = 19
    _r = 9
    _a = pow(_r, 2, _p)
    assert legendre(_a, _p) == 1
    assert legendre(_a, _p) == gmpy2.legendre(_a, _p)
    assert sqrtmod_3_4(_a, _p) == _r
    assert sympy.ntheory.sqrt_mod(_a, _p) == _r

    _p = 13
    _r = 4
    _a = pow(_r, 2, _p)
    assert legendre(_a, _p) == 1
    assert legendre(_a, _p) == gmpy2.legendre(_a, _p)
    assert sqrtmod_5_8(_a, _p) == _r
    assert sympy.ntheory.sqrt_mod(_a, _p) == _r

    assert legendre(_a + 2, _p) == -1
    assert legendre(_a + 2, _p) == gmpy2.legendre(_a + 2, _p)
    assert sympy.ntheory.sqrt_mod(_a + 2, _p) is None
