# see https://www.pycryptodome.org/

# p, q - primes
# n = p * q
# f - Euler function
# f = (p - 1) * (q - 1)
# e - public exponent
# e < f and gmpy2.gcd(e, f) = 1
# d = gmpy2.invert(e, f)  <=>  ed = 1 + kf
# m - plain text (m < n), c - cypher text
# c = pow(m, e, n)
# m = pow(c, d, n) = pow(m , e * d, n)

# public key = (e, n)
# private key = (d, n)


from Crypto.Util.number import getPrime, getRandomNBitInteger
import gmpy2
import string


SYMBOLS = string.ascii_lowercase


def text_to_blocks(text, block_len):
    blocks = []
    for i0 in range(0, len(text), block_len):
        block = 0
        for i1 in range(i0, min(i0 + block_len, len(text))):
            block += SYMBOLS.find(text[i1]) * pow(len(SYMBOLS), i1 % block_len)
        blocks.append(block)
    return blocks


def blocks_to_text(blocks, block_len, text_len):
    text = []
    for block in blocks:
        block_text = []
        for i in range(block_len - 1, -1, -1):
            if len(text) + i < text_len:
                p = pow(len(SYMBOLS), i)
                j = block // p
                block %= p
                block_text.append(SYMBOLS[j])
        text.extend(block_text[::-1])
    return ''.join(text)


def encrypt(m, key, block_len):
    blocks = []
    e, n = key
    for block in text_to_blocks(m, block_len):
        blocks.append(pow(block, e, n))
    return blocks


def decrypt(c, key, block_len, plain_text_len):
    blocks = []
    d, n = key
    for block in c:
        blocks.append(pow(block, d, n))
    return blocks_to_text(blocks, block_len, plain_text_len)


def decrypt_crt(c, d, p, q):
    # precompute for given key
    dp = d % (p - 1)
    dq = d % (q - 1)
    q_inv = gmpy2.invert(q, p)

    mp = pow(c, dp, p)
    mq = pow(c, dq, q)
    h = q_inv * (mp - mq) % p
    return (mq + h * q) % (p * q)


def generate_key(bits):
    return generate_key_with_pq(bits)[:3]


def generate_key_with_pq(bits):
    p, q = getPrime(bits), getPrime(bits)
    n = p * q
    f = (p - 1) * (q - 1)
    while True:
        e = getRandomNBitInteger(bits)
        if e < f and gmpy2.gcd(e, f) == 1:
            break
    d = int(gmpy2.invert(e, f))
    return e, d, n, p, q


if __name__ == '__main__':
    _block_len = 10
    _m = 'nofatebutwhatwemake'

    _blocks = text_to_blocks(_m, _block_len)
    assert _m == blocks_to_text(_blocks, _block_len, len(_m))

    _key = generate_key_with_pq(128)
    _e, _d, _n, _p, _q = _key

    _c = encrypt(_m, (_e, _n), _block_len)
    assert _m == decrypt(_c, (_d, _n), _block_len, len(_m))

    _m = 696969
    _c = pow(_m, _e, _n)
    assert _m == decrypt_crt(_c, _d, _p, _q)
