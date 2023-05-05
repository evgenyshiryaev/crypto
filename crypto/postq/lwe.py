import numpy as np
import random

# As + e == b mod q
# A: Y * X (m * n)
# s: X * 1 - small
# e: X * 1 - small
# b: Y * 1
# (A, b) - public key
# s - secret key

# encrypt
# B' = S'A + E' mod q
# v = S'B + e' + encode(m)
# S', E' and e' - small

# decrypt
# m = v - B's = e + e' + m + E's


def rand_matrix(y, x, q):
    return np.matrix([[random.randint(0, q - 1) for _ in range(x)] for _ in range(y)])


def rand_small_matrix(y, x, max_e):
    return np.matrix([[np.random.default_rng().binomial(max_e * 2, 0.5) - max_e for _ in range(x)] for _ in range(y)])


def generate_key(n, q, max_e):
    A = rand_matrix(n, n, q)
    s = rand_small_matrix(n, 1, max_e)
    e = rand_small_matrix(n, 1, max_e)
    b = (A * s + e) % q
    return (A, b), s


# B' = S'A' + E' mod q
# V = S'B + e' + encode(m)
def encrypt(m, key, q, max_e):
    A, b = key
    n = A.shape[0]

    m = m.hex()
    assert len(m) <= n
    m += '0' * (n - len(m))
    m = [[(q // 2 ** 4) * int(c, 16)] for c in m]
    m = np.matrix(m)

    S1 = rand_small_matrix(n, n, max_e)
    E1 = rand_small_matrix(n, n, max_e)
    e1 = rand_small_matrix(n, 1, max_e)

    B1 = (S1 * A + E1) % q
    v = (S1 * b + e1 + m) % q
    return B1, v


# m = v - B's
def decrypt(c, s, q):
    B1, v = c
    m = (v - B1 * s) % q
    m_hex = ""
    for e in m:
        f = round(int(e[0]) * 2 ** 4 / q) % (2 ** 4)
        m_hex += hex(f)[2:]
    return bytes.fromhex(m_hex)


if __name__ == '__main__':
    _n = 20
    _q = 15901
    _max_e = 10
    _m = b'Secret...'

    _key = generate_key(_n, _q, _max_e)
    _m_enc = encrypt(_m, _key[0], _q, _max_e)
    _m_dec = decrypt(_m_enc, _key[1], _q)
    assert _m + b'\x00' * (_n // 2 - len(_m)) == _m_dec
