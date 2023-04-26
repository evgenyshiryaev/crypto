def gcd(a, b):
    while b:
        a, b = b, a % b
    return a.monic()


def franklin_reiter(n, e, c0, a0, b0, c1, a1, b1):
    R.<X> = Zmod(n)[]  # PolynomialRing(Zmod(n))
    g0 = (a0 * X + b0) ^ e - c0
    g1 = (a1 * X + b1) ^ e - c1
    return int(-gcd(g0, g1).coefficients()[0])


p = random_prime(2 ^ 256)
q = random_prime(2 ^ 256)
n = p * q
e = 3

m = b'This is super secret message noone can read'
pad0 = int.from_bytes(b'some padding', 'big')
pad1 = int.from_bytes(b'just another one', 'big')
c0 = pow(int.from_bytes(m, 'big') + pad0, e, n)
c1 = pow(int.from_bytes(m, 'big') + pad1, e, n)

m_hacked = franklin_reiter(n, e, c0, 1, pad0, c1, 1, pad1)
assert m == m_hacked.to_bytes(len(hex(m_hacked)[2:]) // 2, 'big')
