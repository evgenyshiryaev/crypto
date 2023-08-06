# https://link.springer.com/content/pdf/10.1007/BFb0055716.pdf
# http://secgroup.dais.unive.it/wp-content/uploads/2012/11/Practical-Padding-Oracle-Attacks-on-RSA.html


from Crypto.Util.number import bytes_to_long, long_to_bytes
import portion as I
import random


def ceil(x, y):
    return x // y + (x % y != 0)


# PKCS #1 v1.5
# 00 02 ps 00 m  - padding string, message
# k = |n|  - byte length of n
# 2^8*(k-1) <= n < 2^8*k
# |ps| >= 8
# |ps| = k - 3 - |m|
# |m| <= k - 11

def pad(m, k):
    m_b = long_to_bytes(m)
    assert len(m_b) <= k - 11
    m_p = bytearray()
    m_p.append(0)
    m_p.append(2)
    for _ in range(k - 3 - len(m_b)):
        m_p.append(random.randrange(1, 0x100))
    m_p.append(0)
    m_p += m_b
    assert len(m_p) == k
    return bytes_to_long(m_p)


def unpad(m, k):
    m_b = long_to_bytes(m)
    assert len(m_b) == k - 1  # no leading zero
    assert m_b[0] == 2
    for i in range(1, len(m_b)):
        if m_b[i] == 0:
            break
    assert 8 < i < len(m_b) - 1
    return bytes_to_long(m_b[i + 1:])


def get_k(n):
    return ceil(n.bit_length(), 8)


def get_s(m, n, k, s, s_max=None):
    while s_max is None or s <= s_max:
        try:
            unpad((s * m) % n, k)
            return s
        except AssertionError:
            s += 1
    return None


# s - any
# m*s is PKCS valid
# 00 02 ... <= m*s mod n < 00 03 ...
# B = 2^8*(k-2)
# 2*B <= m*s mod n < 3*B
def hack(n, m):
    k = get_k(n)
    B = pow(2, 8 * (k - 2))
    B2, B3 = 2 * B, 3 * B

    # 2.a
    s = get_s(m, n, k, ceil(n, 3 * B))
    M = I.closed(B2, B3 - 1)

    while len(M) > 1 or M.lower != M.upper:
        if len(M) > 1:
            # 2.b
            s = get_s(m, n, k, s + 1)
        else:
            # 2.c
            a, b = M.lower, M.upper
            r = ceil(2 * (b * s - B2), n)
            s = None
            while s is None:
                s = get_s(m, n, k, ceil(B2 + r * n, b), ceil(B3 + r * n, a) - 1)
                r += 1

        M_next = I.empty()
        for i in M:
            a, b = i.lower, i.upper
            for r in range(ceil(a * s - B3 + 1, n), (b * s - B2) // n + 1):
                M_next |= I.closed(max(a, ceil(B2 + r * n, s)), min(b, (B3 - 1 + r * n) // s))
        M = M_next

    return M.lower


if __name__ == '__main__':
    from crypto.asym.rsa.rsa import generate_key
    _BITS = 512
    _e, _d, _n = generate_key(_BITS)

    _m = bytes_to_long(b'This is too hard to hack')
    _k = get_k(_n)
    _m_p = pad(_m, _k)
    assert _m == unpad(_m_p, _k)

    assert hack(_n, _m_p) == _m_p
