# https://www.davidwong.fr/blockbreakers/square.html

from crypto.aes.aes_helper import *
import random
from tqdm import tqdm


def encrypt(plaintext, key, reduced_nr=None):
    nb = 4  # columns (words) number
    nk = len(key) // 4  # words number comprising key (4, 6 or 8)
    nr = nk + 6  # rounds number
    if reduced_nr is None:
        reduced_nr = nr
    state = bytes_to_state(plaintext)
    w = key_expansion(key, nb, nr, nk)
    add_round_key(state, w, 0, nb)
    for rnd in range(1, reduced_nr + 1):
        sub_bytes(state)
        shift_rows(state)
        if rnd != 4:
            mix_columns(state)
        add_round_key(state, w, rnd, nb)
    return state_to_bytes(state)


def gen_cs(key, rounds):
    m_suffix = random.randbytes(15)
    return [encrypt(i.to_bytes(1, 'big') + m_suffix, key, rounds) for i in range(0x100)]


def hack_1_round():
    key = random.randbytes(16)
    cs = gen_cs(key, 1)
    bs = [set() for _ in range(16)]
    for c in cs:
        for i in range(16):
            bs[i].add(c[i])
    for i in range(4):
        assert len(bs[i]) == 0x100
    for i in range(4, 16):
        assert len(bs[i]) == 1


def hack_2_rounds():
    key = random.randbytes(16)
    cs = gen_cs(key, 2)
    bs = [set() for _ in range(16)]
    for c in cs:
        for i in range(16):
            bs[i].add(c[i])
    for i in range(16):
        assert len(bs[i]) == 0x100


def hack_3_rounds():
    key = random.randbytes(16)
    cs = gen_cs(key, 3)
    bs = [0] * 16
    for c in cs:
        for i in range(16):
            bs[i] ^= c[i]
    for i in range(16):
        assert bs[i] == 0


# https://www.davidwong.fr/blockbreakers/square_2_attack4rounds.html
def hack_4_rounds():
    key = random.randbytes(16)

    key_exp = key_expansion(key, 4, 4, 4)
    key_4 = [key_exp[4 * 4 + i].to_bytes(4, 'big')[j] for i in range(4) for j in range(4)]

    # some sets will generate false positive key bytes
    css = [list(map(bytes_to_state, gen_cs(key, 4)))]

    key_4_hack = []
    for key_i in tqdm(range(16)):
        state_y, state_x = key_i % 4, key_i // 4
        state_i = 0
        while True:
            cs = css[state_i]
            key_bytes = []
            for key_byte in range(0x100):
                b = 0
                for c in cs:
                    b ^= inv_s_box[c[state_y][state_x] ^ key_byte]
                    # same as following but faster
                    # state[state_y][state_x] ^= key_byte
                    # inv_shift_rows(state)
                    # inv_sub_bytes(state)
                    # b ^= state[state_y][state_x_shift]
                if b == 0:
                    key_bytes.append(key_byte)
            if len(key_bytes) == 1:
                key_4_hack.append(key_bytes[0])
                break
            state_i += 1
            if state_i == len(css):
                css.append(list(map(bytes_to_state, gen_cs(key, 4))))
    assert key_4 == key_4_hack, str(key_4) + ' / ' + str(key_4_hack)

    key_exp_hack = inv_key_expansion(key_4_hack, 4, 4, 4)
    key_hack = b''
    for i in range(4):
        key_hack += key_exp_hack[i].to_bytes(4, 'big')
    assert key_hack == key


if __name__ == '__main__':
    hack_1_round()
    hack_2_rounds()
    hack_3_rounds()
    hack_4_rounds()
