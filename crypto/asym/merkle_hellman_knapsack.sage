# https://en.wikipedia.org/wiki/Merkle%E2%80%93Hellman_knapsack_cryptosystem
# https://en.wikipedia.org/wiki/Lenstra%E2%80%93Lenstra%E2%80%93Lov%C3%A1sz_lattice_basis_reduction_algorithm

from Crypto.Util.number import bytes_to_long, long_to_bytes


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
    m = bin(bytes_to_long(m))[2:].rjust(len(B), '0')
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


def lll_hack(c, pub_key):
    B, bits = pub_key, len(pub_key)
    L = identity_matrix(bits)
    L = L.stack(zero_vector(bits))
    L = L.augment(vector(_pub_key + [-c]))
    LR = L.LLL()

    found = False
    for x in LR:
        if all(xi == 0 or xi == 1for xi in x[:-1]) and x[-1] == 0:
            found = True
            break
    if not found:
        print('No good vector')
        return None

    m = b''
    for i in range (0, len(x) - 1, 8):
        m += long_to_bytes(int(''.join([str(b) for b in x[i: i + 8]]), 2))
    print(m)
    return m


if __name__ == '__main__':
    _pub_key, _priv_key = generate_key(256)
    _m = b'soo unsecret'
    _c = encrypt(_m, _pub_key)
    assert _m == decrypt(_c, _priv_key)

    _m = b'soo'
    _pub_key, _priv_key = generate_key(len(_m) * 8)
    _c = encrypt(_m, _pub_key)
    lll_hack(_c, _pub_key)
