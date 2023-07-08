# https://github.com/yud121212/Coppersmith-s-Short-Pad-Attack-Franklin-Reiter-Related-Message-Attack/blob/master/coppersmiths_short_pad_attack.sage
# https://github.com/mimoo/RSA-and-LLL-attacks/blob/master/coppersmith.sage


def generate_key(bits, e):
    while True:
        p, q = random_prime(2 ^ bits), random_prime(2 ^ bits)
        n = p * q
        f = (p - 1) * (q - 1)
        if e < f and gcd(e, f) == 1:
            return n


def short_pad(c0, c1, e, n):
    PRxy.<x,y> = Zmod(n)[]
    PRx.<xn> = Zmod(n)[]
    PRZZ.<xz,yz> = Zmod(n)[]

    g0 = x ^ e - c0
    g1 = (x + y) ^ e - c1

    q0 = g0.change_ring(PRZZ)
    q1 = g1.change_ring(PRZZ)

    h = q1.resultant(q1)
    h = h.univariate_polynomial()
    h = h.change_ring(PRx).subs(y=xn)
    h = h.monic()

    kbits = n.nbits() // (2 * e * e)
    roots = h.small_roots(X=2 ^ kbits, beta=0.5)  # find root < 2^kbits with factor >= n^0.5
    return roots[0] if len(roots) == 1 else None


BITS = 512
e = 3
n = generate_key(BITS, e)
m = getrandbits(BITS)
x = getrandbits(16)
c0 = pow(m, e, n)
c1 = pow(m + x, e, n)

x_hacked = short_pad(c0, c1, e, n)
assert x == x_hacked
