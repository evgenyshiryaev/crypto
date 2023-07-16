# https://en.wikipedia.org/wiki/Merkle%E2%80%93Hellman_knapsack_cryptosystem

from Crypto.Util.number import bytes_to_long, long_to_bytes
from gmpy2 import gcd
from random import randrange


def generate_key(bits, incr=69):
    W, s = [], 0
    for _ in range(bits):
        W.append(s + randrange(0, incr))  # superincreasing knapsack
        s += W[-1]
    q = randrange(s + 1, 2 * s)
    while True:
        r = randrange(1, q)
        if gcd(r, q) == 1:
            break
    B = [r * w % q for w in W]
    return B, (W, q, r)


def encrypt(m, pub_key):
    B = pub_key
    m = bin(bytes_to_long(m))[2:].zfill(len(B))
    return sum([int(mi) * bi for mi, bi in zip(m, B)])


def decrypt(c, priv_key):
    W, q, r = priv_key
    c = c * pow(r, -1, q) % q
    i = len(W) - 1
    x = []
    while c > 0:
        if W[i] <= c:
            x.append(i)
            c -= W[i]
        i -= 1
    return long_to_bytes(sum([2 ** (len(W) - xi - 1) for xi in x]))


if __name__ == '__main__':
    _pub_key, _priv_key = generate_key(256)
    _m = b'soo unsecret'
    _c = encrypt(_m, _pub_key)
    assert _m == decrypt(_c, _priv_key)
