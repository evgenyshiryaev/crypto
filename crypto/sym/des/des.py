# https://russianblogs.com/article/5237992568/
# https://github.com/LyleScott/DES-Encryption-in-Python

# block = 64 bits = 8 bytes
# key = 56 bits = 7 bytes (8 bytes input key parity bits are ignored)

# schema:
#   key expansion
#   initial permutation
#   16 rounds (Feistel)
#   inverse initial permutation

from crypto.sym.des.des_helper import *


def encrypt(plaintext, key):
    return encrypt_decrypt(plaintext, key, True)


def decrypt(ciphertext, key):
    return encrypt_decrypt(ciphertext, key, False)


def encrypt_decrypt(plaintext, key, enc):
    keys = key_expansion(key)
    if not enc:
        keys.reverse()

    data = bytes_to_bin(plaintext)
    data = initial_permutation(data)
    data = feistel(data, keys)
    data = inverse_initial_permutation(data)
    return bin_to_bytes(data)


if __name__ == '__main__':
    import random
    _plaintext = random.randbytes(8)
    _key = random.randbytes(8)
    _ciphertext = encrypt(_plaintext, _key)
    assert _plaintext == decrypt(_ciphertext, _key)

    from Crypto.Cipher import DES
    assert _ciphertext == DES.new(_key, DES.MODE_ECB).encrypt(_plaintext)
