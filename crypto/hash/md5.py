# https://en.wikipedia.org/wiki/MD5

# hash = 128 bits = 16 bytes
# block = 512 bits = 64 bytes = 16 dwords
# rounds = 4


from math import floor, sin
from utils.bits import INT_BYTES, INT_MAX, LONG_BYTES, LONG_MAX, rotate_left


class md5:
    BLOCK_SIZE = 64
    S = (7, 12, 17, 22) * 4 + (5, 9, 14, 20) * 4 + (4, 11, 16, 23) * 4 + (6, 10, 15, 21) * 4
    K = tuple([floor((INT_MAX + 1) * abs(sin(i + 1))) for i in range(64)])
    STATE = (0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476)

    @staticmethod
    def digest(data, init_state=None, init_len=0):
        data_len = len(data)
        if init_len > 0:
            add_len = init_len
            if init_len % md5.BLOCK_SIZE != 0:
                add_len += md5.BLOCK_SIZE - init_len % md5.BLOCK_SIZE
            data_len += add_len

        data += md5.padding(data_len)
        assert len(data) % md5.BLOCK_SIZE == 0

        if init_state is None:
            state = list(md5.STATE)
        else:
            assert len(init_state) == 4 * INT_BYTES
            state = []
            for i in range(0, len(init_state), INT_BYTES):
                state.append(int.from_bytes(init_state[i: i + INT_BYTES], 'little'))

        for chunk_start in range(0, len(data), md5.BLOCK_SIZE):
            chunk = data[chunk_start: chunk_start + md5.BLOCK_SIZE]

            a = state[0]
            b = state[1]
            c = state[2]
            d = state[3]

            for i in range(md5.BLOCK_SIZE):
                if i < 16:
                    f = (b & c) | (~b & d)
                    g = i
                elif i < 32:
                    f = (d & b) | (~d & c)
                    g = ((5 * i) + 1) % 16
                elif i < 48:
                    f = b ^ c ^ d
                    g = ((3 * i) + 5) % 16
                else:
                    f = c ^ (b | ~d)
                    g = (7 * i) % 16
                m = int.from_bytes(chunk[4 * g: 4 * g + 4], 'little')
                f = (f + a + md5.K[i] + m) & INT_MAX
                a, b, c, d = d, (b + rotate_left(f, md5.S[i])) & INT_MAX, b, c

            state[0] = (state[0] + a) & INT_MAX
            state[1] = (state[1] + b) & INT_MAX
            state[2] = (state[2] + c) & INT_MAX
            state[3] = (state[3] + d) & INT_MAX

        r = b''
        for s in state:
            r += s.to_bytes(INT_BYTES, 'little')
        return r

    @staticmethod
    def padding(data_len):
        p = b'\x80'
        while (data_len + len(p)) % md5.BLOCK_SIZE != md5.BLOCK_SIZE - LONG_BYTES:
            p += b'\x00'
        return p + ((data_len * 8) & LONG_MAX).to_bytes(LONG_BYTES, 'little')


if __name__ == '__main__':
    import hashlib
    import random
    _data0 = random.randbytes(random.randint(1, 1000000))
    _data0_md5 = md5.digest(_data0)
    assert _data0_md5 == hashlib.md5(_data0).digest()

    _data1 = random.randbytes(random.randint(1, 1000000))
    _data_md5 = md5.digest(_data1, _data0_md5, len(_data0))
    assert _data_md5 == hashlib.md5(_data0 + md5.padding(len(_data0)) + _data1).digest()
