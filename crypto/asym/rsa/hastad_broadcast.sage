def generate_key(bits, e):
    while True:
        p, q = random_prime(2 ^ bits), random_prime(2 ^ bits)
        n = p * q
        f = (p - 1) * (q - 1)
        if e < f and gcd(e, f) == 1:
            return n


def hastad_broadcast(e, ns, cs, ai, bi):
    ts = []
    t_mods = [0] * e
    for i in range(e):
        t_mods[i] = 1
        ts.append(crt(t_mods, ns))
        t_mods[i] = 0

    G.<x> = Zmod(prod(ns))[]
    gs = []
    for i in range(e):
        g = (ts[i] * ((ai[i] * x + bi[i]) ** e - cs[i]))
        gs.append(g)

    g = sum(gs).monic()
    roots = g.small_roots()
    return roots[0]


BITS = 256
e = 3
ns = [generate_key(BITS, e) for _ in range(e)]
m = getrandbits(BITS)

ai = [randint(0, ns[i] - 1) for i in range(e)]  # gcd(a, n) should be 1
bi = [randint(0, ns[i] - 1) for i in range(e)]
cs = [Integer(pow(ai[i] * m + bi[i], e, ns[i])) for i in range(e)]  # case to Integer is important

m_hacked = hastad_broadcast(e, ns, cs, ai, bi)
assert m == m_hacked
