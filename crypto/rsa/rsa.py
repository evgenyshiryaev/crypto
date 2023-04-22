# see https://www.pycryptodome.org/

# n = p * q
# f = (p - 1) * (q - 1)
# e: e < f and gmpy2.gcd(e, f) = 1
# d = gmpy2.invert(e, f)  <=>  ed = 1 + kf
# c = m ^ e % n (m < n)
# m = c ^ d % n = m ^ ed % n
# public key = (e, n)
# private key = (d, n)

import Crypto.Util.number
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


def encrypt(plain_text, key, block_len):
    blocks = []
    e, n = key
    for block in text_to_blocks(plain_text, block_len):
        blocks.append(pow(block, e, n))
    return blocks


def decrypt(cipher_text, key, block_len, plain_text_len):
    blocks = []
    d, n = key
    for block in cipher_text:
        blocks.append(pow(block, d, n))
    return blocks_to_text(blocks, block_len, plain_text_len)


def generate_key(bits):
    p = Crypto.Util.number.getPrime(bits)
    q = Crypto.Util.number.getPrime(bits)
    n = p * q
    f = (p - 1) * (q - 1)
    while True:
        e = Crypto.Util.number.getRandomNBitInteger(bits)
        if e < f and gmpy2.gcd(e, f) == 1:
            break
    d = int(gmpy2.invert(e, f))
    return e, d, n


if __name__ == '__main__':
    _block_len = 10

    _plain_text = 'nofatebutwhatwemake'
    print(_plain_text)

    _blocks = text_to_blocks(_plain_text, _block_len)
    print(_blocks)
    print(blocks_to_text(_blocks, _block_len, len(_plain_text)))

    _bits = 32
    _key = generate_key(_bits)
    print(_key)
    _e, _d, _n = _key

    _cipher_text = encrypt(_plain_text, (_e, _n), _block_len)
    print(_cipher_text)

    print(decrypt(_cipher_text, (_d, _n), _block_len, len(_plain_text)))
