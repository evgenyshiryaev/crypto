# https://www.rieselprime.de/ziki/Modular_square_root
# see nummaster.basic.sqrtmod
# see sympy.ntheory.sqrt_mod

# r^2 = a mod m

def legendre(a, m):
    return pow(a, (m - 1) // 2, m)


# m = 3 mod 4
def sqrtmod_3_4(a, m):
    assert m % 4 == 3
    return pow(a, (m + 1) // 4, m)


# m = 5 mod 8
def sqrtmod_5_8(a, m):
    assert m % 8 == 5
    v = pow(2 * a, (m - 5) // 8, m)
    i = (2 * a * v * v) % m
    return (a * v * (i - 1)) % m


# m = 1 mod 8
def sqrtmod_1_8(a, m):
    assert m % 8 == 1
    pass


if __name__ == '__main__':
    from nummaster.basic import sqrtmod

    _m = 19
    _r = 9
    _a = pow(_r, 2, _m)
    assert legendre(_a, _m) == 1
    assert sqrtmod_3_4(_a, _m) == _r
    assert sqrtmod(_a, _m) == _r

    _m = 13
    _r = 9
    _a = pow(_r, 2, _m)
    assert legendre(_a, _m) == 1
    assert sqrtmod_5_8(_a, _m) == _r
    assert sqrtmod(_a, _m) == _r

    assert legendre(_a + 2, _m) == _m - 1

