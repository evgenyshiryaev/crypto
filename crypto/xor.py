from pwn import *


# ETAOIN SHRDLU
m = {
    ord(' '): 3,
    ord('E'): 2, ord('e'): 2,
    ord('T'): 2, ord('t'): 2,
    ord('A'): 2, ord('a'): 2,
    ord('O'): 2, ord('o'): 2,
    ord('I'): 2, ord('i'): 2,
    ord('N'): 2, ord('n'): 2,
    ord('S'): 1, ord('s'): 1,
    ord('H'): 1, ord('h'): 1,
    ord('R'): 1, ord('r'): 1,
    ord('D'): 1, ord('d'): 1,
    ord('L'): 1, ord('l'): 1,
    ord('U'): 1, ord('u'): 1,
}


def hamming(s0, s1):
    assert len(s0) == len(s1)
    return sum((c0 ^ c1).bit_count() for c0, c1 in zip(s0, s1))


def key_sizes(enc, max_size=40, count=3):
    r = []  # min pairs (normalized hamming, hey_size)
    for key_size in range(2, max_size + 1):
        h = []
        for start in range(0, len(enc) - 2 * key_size, 2 * key_size):
            h.append(hamming(enc[start: start + key_size], enc[start + key_size: start + 2 * key_size]))
        h = sum(h) / len(h) / key_size

        print(key_size, h)
        if len(r) == count and h < r[2][0]:
            r.pop(count - 1)
        if len(r) < count:
            r.append((h, key_size))
            r.sort()
    return tuple(map(lambda x: x[1], r))


def solve_single_xor(enc):
    best_key = -1
    best_score = 0
    for key in range(256):
        score = 0
        for enc_byte in enc:
            dec_byte = key ^ enc_byte
            if dec_byte in m:
                score += m[dec_byte]
        if score > best_score:
            best_score = score
            best_key = key
    return best_key, best_score
