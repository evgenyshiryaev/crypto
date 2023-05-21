from crypto.block.des.des_constants import *


# main functions

# convert bytes to bin with '0' padding to 64 bits length
def bytes_to_bin(data):
    return str(bin(int.from_bytes(data, 'big')))[2:].rjust(64, '0')


def key_expansion(key):
    keys = []
    key = bytes_to_bin(key)
    key = permutation(key, pc1)
    for i in range(1, 17):
        first, second = key[:28], key[28:]
        first = first[lshift[i - 1]:] + first[:lshift[i - 1]]
        second = second[lshift[i - 1]:] + second[:lshift[i - 1]]
        key = first + second
        keys.append(permutation(key, pc2))
    return keys


def initial_permutation(data):
    return permutation(data, ip)


def inverse_initial_permutation(data):
    return permutation(data, inv_ip)


def feistel(data, keys):
    for i in range(16):
        left, right = data[:32], data[32:]
        data = right + xor(left, f(right, keys, i))
    return data[32:] + data[:32]


def bin_to_bytes(data):
    return int(data, 2).to_bytes(8, 'big')


# helpers

def permutation(data, p_box):
    # not always len(data) == len(p_box)
    return ''.join([data[i - 1] for i in p_box])


def f(data, keys, rnd):
    data = [data[i - 1] for i in e]
    data = xor(data, keys[rnd])
    data = s_box_replace(data)
    return permutation(data, p)


def xor(a, b):
    assert len(a) == len(b)
    return ''.join(['0' if ai == bi else '1' for ai, bi in zip(a, b)])


def s_box_replace(data):
    r = ''
    for i in range(8):
        row = int(data[i * 6] + data[i * 6 + 5], 2)
        line = int(data[i * 6 + 1: i * 6 + 5], 2)
        r += str(bin(s_boxs[i][row][line]))[2:].rjust(4, '0')
    return r
