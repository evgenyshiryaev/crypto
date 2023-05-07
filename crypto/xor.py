# ETAOIN SHRDLU
ETAOIN = {
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
            if dec_byte in ETAOIN:
                score += ETAOIN[dec_byte]
        if score > best_score:
            best_score = score
            best_key = key
    return best_key, best_score


def mtp(cs):
    c_len = len(cs[0])
    cs_len = len(cs)
    ms = [[0] * c_len for _ in range(cs_len)]

    mtp_space(cs, ms)

    known_chars = []  # [(cs_i, c_i, c)]. Ex - [(1, 0, ord('E'))]
    mtp_known_chars(cs, ms, known_chars)

    return [bytearray(m) for m in ms]


# 00100000 _ 20
# 01000001 A 41
# 01100001 a 61
# 01111010 z 7a
# [A-Za-z] ^ _ >= 0x40
# [A-Za-z] ^ [A-Za-z] < 0x40
def mtp_space(cs, ms):
    c_len = len(cs[0])
    cs_len = len(cs)

    for cs_i in range(cs_len):
        for c_i in range(c_len):
            if ms[cs_i][c_i] != 0:
                continue

            space = True
            for cs_j in range(cs_len):
                x = cs[cs_i][c_i] ^ cs[cs_j][c_i]
                if x != 0 and x < 0x40:
                    space = False
                    break
            if space:
                ms[cs_i][c_i] = 0x20
                for cs_j in range(cs_len):
                    if ms[cs_j][c_i] == 0:
                        ms[cs_j][c_i] = cs[cs_i][c_i] ^ cs[cs_j][c_i] ^ 0x20


def mtp_known_chars(cs, ms, known_chars):
    for cs_i, c_i, c in known_chars:
        if ms[cs_i][c_i] == 0:
            ms[cs_i][c_i] = c
            for cs_j in range(len(cs)):
                if ms[cs_j][c_i] == 0:
                    ms[cs_j][c_i] = cs[cs_i][c_i] ^ cs[cs_j][c_i] ^ c


if __name__ == '__main__':
    _cs = [bytes.fromhex('c909eb881127081823ecf53b383e8b6cd1a8b65e0b0c3bacef53d83f80fb'),
           bytes.fromhex('cf00ec8a5635095d33bfa12a317bc2789eabf95e090c29abe81dd4339ffb'),
           bytes.fromhex('c700ec851e72124b6afef52c3f37cf2bcda9f74202426fa2f54f9c3797fb'),
           bytes.fromhex('cd0ebe8718365b4f2bebb6277039c469dfecf05419586fb4f658dd2997fb'),
           bytes.fromhex('c341ff8b562114552ff0bb2a702cc3649ea0ff5a085f6fb0f51dd93b86f4'),
           bytes.fromhex('da13f1801321085738bf9e2e24218b7fdfb9f159190c22a1ba49d43381fb'),
           bytes.fromhex('cb0df2c63f721c573ebfba21702fc36e9ea9ee50000c38a5e91ddd7ab0fb'),
           bytes.fromhex('c913e796023d1c4a2befbd367032d82bdfecf55e02406fa7f548ce2997f4')]
    print(mtp(_cs))
