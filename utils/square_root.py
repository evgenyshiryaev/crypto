# https://www.rieselprime.de/ziki/Modular_square_root
# see sympy.ntheory.sqrt_mod
# see nummaster.basic.sqrtmod

# r^2 = a mod m

# (a/m)
# https://en.wikipedia.org/wiki/Legendre_symbol
# use gmpy2.legendre()
def legendre(a, m):
    if a % m == 0:
        return 0
    return 1 if pow(a, (m - 1) // 2, m) == 1 else -1


# m = 3 mod 4
def sqrtmod_3_4(a, m):
    assert m % 4 == 3
    return min_root(pow(a, (m + 1) // 4, m), m)


# m = 5 mod 8
def sqrtmod_5_8(a, m):
    assert m % 8 == 5
    v = pow(2 * a, (m - 5) // 8, m)
    i = (2 * a * v * v) % m
    return min_root((a * v * (i - 1)) % m, m)


# m = 1 mod 8
def sqrtmod_1_8(a, m):
    assert m % 8 == 1
    pass


def min_root(r, m):
    return min(r, -r % m)


if __name__ == '__main__':
    import sympy.ntheory
    import gmpy2

    _m = 19
    _r = 9
    _a = pow(_r, 2, _m)
    assert legendre(_a, _m) == 1
    assert legendre(_a, _m) == gmpy2.legendre(_a, _m)
    assert sqrtmod_3_4(_a, _m) == _r
    assert sympy.ntheory.sqrt_mod(_a, _m) == _r

    _m = 13
    _r = 4
    _a = pow(_r, 2, _m)
    assert legendre(_a, _m) == 1
    assert legendre(_a, _m) == gmpy2.legendre(_a, _m)
    assert sqrtmod_5_8(_a, _m) == _r
    assert sympy.ntheory.sqrt_mod(_a, _m) == _r

    assert legendre(_a + 2, _m) == -1
    assert legendre(_a + 2, _m) == gmpy2.legendre(_a + 2, _m)
    assert sympy.ntheory.sqrt_mod(_a + 2, _m) is None
