def gcd(a, b):
    return a if b == 0 else gcd(b, a % b)


def lcm(a, b):
    return a // gcd (a, b) * b


# a * x + b * y = gcd(a, b)
def gcdExt(a, b):
    if a == 0:
        return b, 0, 1

    d, x, y = gcdExt(b % a, a)
    return d, y - (b // a) * x, x


# a * b = 1 mod m
def mmi(a, m):
    d, x, _ = gcdExt(a, m)
    return 0 if d != 1 else x % m


# (a mod m) / b
def divMod(a, b, m):
    i = mmi(b, m)
    return (a * i) % m


if __name__ == "__main__":
    print(gcd(15, 25))
    print(lcm(4, 10))
    print(gcdExt(15, 25))
