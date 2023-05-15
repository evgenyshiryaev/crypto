from crypto.aes.aes_constants import *


def bytes_to_state(data):
    return [[data[i], data[i + 4], data[i + 8], data[i + 12]] for i in range(4)]


def state_to_bytes(state):
    data = b''
    for x in range(4):
        for y in range(4):
            data += state[y][x].to_bytes(1, 'big')
    return data


# https://www.davidwong.fr/blockbreakers/aes_4_key_scheduler.html
# https://camo.githubusercontent.com/77e8022c3c0518d1849d94611dccf3d0c9d3a2694b34ef99a2189f12153686c7/68747470733a2f2f692e696d6775722e636f6d2f5a4a3375576b492e6a7067
# zero round key to key scheduling
def key_expansion(key, nb, nr, nk):
    # w0 - w43 for AES-128 (4 * 11)
    w = [None] * nb * (nr + 1)

    # init round 0 key
    for i in range(nk):
        w[i] = word((key[4 * i], key[4 * i + 1], key[4 * i + 2], key[4 * i + 3]))

    for i in range(nk, len(w)):
        temp = w[i - 1]
        if i % nk == 0:
            # https://www.davidwong.fr/blockbreakers/aes_3_rcon.html
            temp = sub_word(rot_word(temp)) ^ r_con[i // nk]
        elif nk == 8 and i % nk == 4:
            temp = sub_word(temp)
        w[i] = w[i - nk] ^ temp

    return w


# last round key to key scheduling
# !!! implemented for AES-128 only !!!
def inv_key_expansion(key, nb, nr, nk):
    w = [None] * nb * (nr + 1)

    # init last round key
    for i in range(nk):
        w[len(w) - nk + i] = word((key[4 * i], key[4 * i + 1], key[4 * i + 2], key[4 * i + 3]))

    for i in range(len(w) - nk - 1, -1, -1):
        temp = w[i + nk - 1]
        if i % nk == 0:
            temp = sub_word(rot_word(temp)) ^ r_con[i // nk + 1]
        w[i] = temp ^ w[i + nk]

    return w


def word(bs):
    return int.from_bytes(bytearray(bs), 'big')


# https://www.davidwong.fr/blockbreakers/aes_2_subword.html
def sub_word(w):
    bs = [w >> i & 0xff for i in (24, 16, 8, 0)]
    return word([s_box[bs[i]] for i in range(4)])


# https://www.davidwong.fr/blockbreakers/aes_1_rotword.html
def rot_word(w):
    bs = [w >> i & 0xff for i in (24, 16, 8, 0)]
    return word((bs[1], bs[2], bs[3], bs[0]))


# https://www.davidwong.fr/blockbreakers/aes_6_subbytes.html
def sub_bytes(state):
    sub_bytes_helper(state, s_box)


def inv_sub_bytes(state):
    sub_bytes_helper(state, inv_s_box)


def sub_bytes_helper(state, sub):
    for y in range(4):
        for x in range(4):
            state[y][x] = sub[state[y][x]]


# https://www.davidwong.fr/blockbreakers/aes_7_shiftrows.html
def shift_rows(state):
    # do nothing with state[0]
    state[1][0], state[1][1], state[1][2], state[1][3] = state[1][1], state[1][2], state[1][3], state[1][0]
    state[2][0], state[2][1], state[2][2], state[2][3] = state[2][2], state[2][3], state[2][0], state[2][1]
    state[3][0], state[3][1], state[3][2], state[3][3] = state[3][3], state[3][0], state[3][1], state[3][2]


def inv_shift_rows(state):
    # do nothing with state[0]
    state[1][0], state[1][1], state[1][2], state[1][3] = state[1][3], state[1][0], state[1][1], state[1][2]
    state[2][0], state[2][1], state[2][2], state[2][3] = state[2][2], state[2][3], state[2][0], state[2][1]
    state[3][0], state[3][1], state[3][2], state[3][3] = state[3][1], state[3][2], state[3][3], state[3][0]


# https://www.davidwong.fr/blockbreakers/aes_8_mixcolumns.html
def mix_columns(state):
    mix_columns_helper(state, ax)


def inv_mix_columns(state):
    mix_columns_helper(state, inv_ax)


def mix_columns_helper(state, m):
    for x in range(4):
        rows = [0, 0, 0, 0]

        for y in range(4):
            rows[0] ^= ff_multiply(m[0][y], state[y][x])
            rows[1] ^= ff_multiply(m[1][y], state[y][x])
            rows[2] ^= ff_multiply(m[2][y], state[y][x])
            rows[3] ^= ff_multiply(m[3][y], state[y][x])

        for y in range(4):
            state[y][x] = rows[y]


# multiply two finite fields
def ff_multiply(a, b):
    r = 0
    for i in range(8):
        if a == 0 or b == 0:
            break
        if a & 1:
            r ^= b
        b = xtime(b)
        a >>= 1
    return r


# multiply the given polynomial (finite field) by x
def xtime(a):
    b = a << 1
    if a & (1 << 7):
        b = (b ^ 0x1b) & 0xff
    return b


# https://www.davidwong.fr/blockbreakers/aes_9_addroundkey.html
def add_round_key(state, w, rnd, nb):
    for x in range(4):
        bs = w[rnd * nb + x].to_bytes(4, 'big')
        for y in range(4):
            state[y][x] ^= bs[y]


if __name__ == '__main__':
    import random

    # AES-128
    _key = random.randbytes(16)
    # print(_key.hex())
    _key_exp = key_expansion(_key, 4, 10, 4)
    # for _k in _key_exp:
    #     print(hex(_k), end=' ')
    # print()
    _key10 = b''
    for _i in range(-4, 0):
        _key10 += _key_exp[_i].to_bytes(4, 'big')
    # print(_key10.hex())
    _inv_key_exp = inv_key_expansion(_key10, 4, 10, 4)
    # for _k in _inv_key_exp:
    #     print(hex(_k), end=' ')
    # print()
    assert _key_exp == _inv_key_exp
