# use gmpy2.gcd()
def gcd(a, b):
    return a if b == 0 else gcd(b, a % b)


# use gmpy2.lcm()
def lcm(a, b):
    return a // gcd(a, b) * b


# use gmpy2.gcdext()
# a * x + b * y = gcd(a, b)
def gcdext(a, b):
    if a == 0:
        return b, 0, 1
    d, x, y = gcdext(b % a, a)
    return d, y - (b // a) * x, x


# use gmpy2.invert() or pow(a, -1, m)
# a * b = 1 mod m
# 0 if gcd(a, m) != 1
def invert(a, m):
    d, x, _ = gcdext(a, m)
    return 0 if d != 1 else x % m


# use gmpy2.divm()
# (a mod m) / b
def divm_deprecated(a, b, m):
    i = invert(b, m)
    return (a * i) % m


if __name__ == '__main__':
    import gmpy2

    assert gcd(15, 25) == gmpy2.gcd(15, 25)
    assert lcm(4, 10) == gmpy2.lcm(4, 10)
    assert gcdext(15, 25) == gmpy2.gcdext(15, 25)
    assert invert(7, 15) == gmpy2.invert(7, 15)
    assert divm_deprecated(7, 11, 15) == gmpy2.divm(7, 11, 15)
