# https://en.wikipedia.org/wiki/Digital_Signature_Algorithm


from Crypto.Util.number import getPrime, isPrime, getRandomNBitInteger
import random

LNS = ((1024, 160), (2048, 224), (2048, 256), (3072, 256))


def generate_params(L, N):
    q = getPrime(N)
    while True:
        m = getRandomNBitInteger(L - N)
        p = q * m + 1
        if isPrime(p) and p.bit_length() == L:
            break
    while True:
        h = random.randrange(2, p - 1)
        g = pow(h, m, p)
        if g != 1:
            return p, q, g


def generate_key(p, q, g):
    x = random.randrange(1, q)  # private key
    y = pow(g, x, p)            # public key
    return x, y


def sign(p, q, g, x, h):
    while True:
        k = random.randrange(1, q)
        r = pow(g, k, p) % q
        if r == 0:
            continue
        s = pow(k, -1, q) * (h + x * r) % q
        if s == 0:
            continue
        return r, s


def verify(p, q, g, y, h, r, s):
    if not 0 < r < q or not 0 < s < q:
        return False
    w = pow(s, -1, q)
    u1, u2 = h * w % q, r * w % q
    v = (pow(g, u1, p) * pow(y, u2, p) % p) % q
    return v == r


if __name__ == '__main__':
    import hashlib
    _h = int(hashlib.sha512(b'Some message to sign with love').hexdigest(), 16)

    _p, _q, _g = generate_params(*LNS[0])
    _x, _y = generate_key(_p, _q, _g)
    _r, _s = sign(_p, _q, _g, _x, _h)
    assert verify(_p, _q, _g, _y, _h, _r, _s)
