def gcd(a, b):
    while b:
        a, b = b, a % b
    return a.monic()


def franklin_reiter(n, e, c0, a0, b0, c1, a1, b1):
    R.<X> = Zmod(n)[]  # PolynomialRing(Zmod(n))
    g0 = (a0 * X + b0) ^ e - c0
    g1 = (a1 * X + b1) ^ e - c1
    return int(-gcd(g0, g1).coefficients()[0])


BITS = 256
p, q = random_prime(2 ^ BITS), random_prime(2 ^ BITS)
n = p * q
e = 3

m = getrandbits(BITS)
pad0 = getrandbits(randint(0, BITS))
pad1 = getrandbits(randint(0, BITS))
c0 = pow(m + pad0, e, n)
c1 = pow(m + pad1, e, n)

m_hacked = franklin_reiter(n, e, c0, 1, pad0, c1, 1, pad1)
assert m == m_hacked
