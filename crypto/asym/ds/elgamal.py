# https://en.wikipedia.org/wiki/ElGamal_signature_scheme


from Crypto.Util.number import getPrime
import gmpy2
import random


# (p, g) - public params
# x - private key
# y - public key
def generate_key(bits):
    p = getPrime(bits)
    g = random.randrange(2, p)
    x = random.randrange(2, p - 1)
    y = pow(g, x, p)
    return (p, g), x, y


def sign(p, g, x, h):
    while True:
        k = random.randrange(2, p - 1)
        if gmpy2.gcd(k, p - 1) == 1:
            r = pow(g, k, p)
            s = (h - x * r) * pow(k, -1, p - 1) % (p - 1)
            if s != 0:
                return r, s


def verify(p, g, y, h, r, s):
    return 0 < r < p and 0 < s < p - 1 \
        and pow(g, h, p) == pow(y, r, p) * pow(r, s, p) % p


def forgery(p, g, y):
    e = random.randrange(2, p - 1)
    while True:
        v = random.randrange(1, p - 1)  # v == 1 is for one-param forgery
        if gmpy2.gcd(v, p - 1) == 1:
            break
    r = pow(g, e, p) * pow(y, v, p) % p
    s = -r * pow(v, -1, p - 1) % (p - 1)
    h = s * e % (p - 1)
    assert verify(p, g, y, h, r, s)


if __name__ == '__main__':
    _BITS = 512
    (_p, _g), _x, _y = generate_key(_BITS)
    _h = random.randrange(2, _p)
    _r, _s = sign(_p, _g, _x, _h)
    assert verify(_p, _g, _y, _h, _r, _s)

    forgery(_p, _g, _y)
