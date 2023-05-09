# https://github.com/joeylemon/python-aes

# block = 128 bits = 16 bytes = 4 x 4 matrix
# AES-128 - 128 bits = 16 bytes key, 10 rounds
# AES-192 - 192 bits = 24 bytes key, 12 rounds
# AES-256 - 259 bits = 32 bytes, 14 rounds

# round operations:
# - SubBytes
# - ShiftRows
# - MixColumns (except final round)
# - AddRoundKey

from crypto.aes.aes_helper import *


def encrypt(plaintext, key):
    nb = 4  # columns (words) number
    nk = len(key) // 4  # words number comprising key (4, 6 or 8)
    nr = nk + 6  # rounds number

    state = bytes_to_state(plaintext)
    w = key_expansion(key, nb, nr, nk)

    add_round_key(state, w, 0, nb)

    for rnd in range(1, nr + 1):
        sub_bytes(state)
        shift_rows(state)
        if rnd != nr:
            mix_columns(state)
        add_round_key(state, w, rnd, nb)

    return state_to_bytes(state)


def decrypt(ciphertext, key):
    nb = 4  # columns (words) number
    nk = len(key) // 4  # words number comprising key (4, 6 or 8)
    nr = nk + 6  # rounds number

    state = bytes_to_state(ciphertext)
    w = key_expansion(key, nb, nr, nk)

    add_round_key(state, w, nr, nb)

    for r in range(nr - 1, -1, -1):
        inv_shift_rows(state)
        inv_sub_bytes(state)
        add_round_key(state, w, r, nb)
        if r != 0:
            inv_mix_columns(state)

    return state_to_bytes(state)


if __name__ == '__main__':
    import random
    _plaintext = random.randbytes(16)
    _key = random.randbytes(16)
    _ciphertext = encrypt(_plaintext, _key)
    assert _plaintext == decrypt(_ciphertext, _key)

    from Crypto.Cipher import AES
    assert _ciphertext == AES.new(_key, AES.MODE_ECB).encrypt(_plaintext)
