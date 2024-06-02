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


def meet_in_the_middle_hack(c, pub_key):
    bits = len(pub_key)

    bits_half, middle, result = bits // 2, {}, None

    def left(i, m, m_c):
        if i == bits_half:
            middle[m_c] = m
        else:
            left(i + 1, m << 1, m_c)
            left(i + 1, (m << 1) | 1, m_c + pub_key[i])

    def right(i, m, m_c):
        nonlocal result
        if result:
            return
        if i == bits:
            m_c0 = c - m_c
            if m_c0 in middle:
                result = middle[m_c0], m
        else:
            right(i + 1, m << 1, m_c)
            right(i + 1, (m << 1) | 1, m_c + pub_key[i])

    left(0, 1, 0)
    right(bits_half, 1, 0)

    x = bin(result[0])[3:] + bin(result[1])[3:]
    m = b''
    for _i in range(0, len(x), 8):
        m += long_to_bytes(int(''.join([str(_b) for _b in x[_i: _i + 8]]), 2))
    return m


if __name__ == '__main__':
    _pub_key, _priv_key = generate_key(256)
    _m = b'soo unsecret'
    _c = encrypt(_m, _pub_key)
    assert _m == decrypt(_c, _priv_key)

    _pub_key, _ = generate_key(48)  # not more
    _m = b'hack01'
    _c = encrypt(_m, _pub_key)
    assert _m == meet_in_the_middle_hack(_c, _pub_key)
