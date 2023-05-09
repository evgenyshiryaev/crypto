# https://github.com/UMD-CSEC/UMDCTF-Public-Challenges/tree/main/UMDCTF2022/crypto/DFA-AES
# https://www.researchgate.net/publication/221005703_DFA_on_AES

from crypto.aes.aes_helper import *
import random
from pwn import xor


# see crypto.aes.aes.encrypt()
def encrypt(plaintext, key, dfa_state_i=None, dfa_bit=None):
    nb = 4  # columns (words) number
    nk = len(key) // 4  # words number comprising key (4, 6 or 8)
    nr = nk + 6  # rounds number

    state = bytes_to_state(plaintext)
    w = key_expansion(key, nb, nr, nk)

    add_round_key(state, w, 0, nb)

    for rnd in range(1, nr + 1):
        # introduce DFA bit fault
        if dfa_state_i is not None and rnd == nr:
            state[dfa_state_i // 4][dfa_state_i % 4] ^= (1 << dfa_bit)

        sub_bytes(state)
        shift_rows(state)
        if rnd != nr:
            mix_columns(state)
        add_round_key(state, w, rnd, nb)

    return state_to_bytes(state)


def get_k10(c, c_faults):
    k10 = [0] * 16
    for c_fault_i in range(0, 16 * 8, 8):
        x = xor(c, c_faults[c_fault_i])
        for fault_byte_i in range(16):
            if x[fault_byte_i]:
                break

        for key_byte in range(0x100):
            # all potential m fault bytes
            m_bytes = [inv_s_box[c_faults[c_fault_i + j][fault_byte_i] ^ key_byte] for j in range(8)]

            # check if there single possible m
            if m_bytes[0] & 0xf0 == m_bytes[1] & 0xf0 and \
                    m_bytes[1] & 0xf0 == m_bytes[2] & 0xf0 and \
                    m_bytes[2] & 0xf0 == m_bytes[3] & 0xf0 and \
                    m_bytes[4] & 0x0f == m_bytes[5] & 0x0f and \
                    m_bytes[5] & 0x0f == m_bytes[6] & 0x0f and \
                    m_bytes[6] & 0x0f == m_bytes[7] & 0x0f:
                break
        k10[fault_byte_i] = key_byte
    return bytearray(k10)


if __name__ == '__main__':
    _m = random.randbytes(16)
    _key = random.randbytes(16)

    _c = encrypt(_m, _key)
    _c_faults = [encrypt(_m, _key, _dfa_state_i, _dfa_bit) for _dfa_state_i in range(16) for _dfa_bit in range(8)]

    _key10 = get_k10(_c, _c_faults)

    _key_exp = inv_key_expansion(_key10, 4, 10, 4)

    _key0 = b''
    for _i in range(4):
        _key0 += _key_exp[_i].to_bytes(4, 'big')
    assert _key == _key0
