import gmpy2


# use gmpy2.gcd()
def gcd_deprecated(a, b):
    return a if b == 0 else gcd_deprecated(b, a % b)


# use gmpy2.lcm()
def lcm_deprecated(a, b):
    return a // gcd_deprecated(a, b) * b


# use gmpy2.gcdext()
# a * x + b * y = gcd(a, b)
def gcdext_deprecated(a, b):
    if a == 0:
        return b, 0, 1
    d, x, y = gcdext_deprecated(b % a, a)
    return d, y - (b // a) * x, x


# use gmpy2.invert()
# a * b = 1 mod m
# 0 if gcd(a, m) != 1
def invert_deprecated(a, m):
    d, x, _ = gcdext_deprecated(a, m)
    return 0 if d != 1 else x % m


# use gmpy2.divm()
# (a mod m) / b
def divm_deprecated(a, b, m):
    i = invert_deprecated(b, m)
    return (a * i) % m


if __name__ == "__main__":
    assert gcd_deprecated(15, 25) == gmpy2.gcd(15, 25)
    assert lcm_deprecated(4, 10) == gmpy2.lcm(4, 10)
    assert gcdext_deprecated(15, 25) == gmpy2.gcdext(15, 25)
    assert invert_deprecated(7, 15) == gmpy2.invert(7, 15)
    assert divm_deprecated(7, 11, 15) == gmpy2.divm(7, 11, 15)
