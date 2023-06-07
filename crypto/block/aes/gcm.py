# https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-38d.pdf
# https://github.com/cgossi/fundamental_cryptography_with_python/blob/main/implementing_aes_gcm.py
# https://www.youtube.com/watch?v=ruJPGDZ6bNA

# iv = 96 bits = 12 bytes
# tag = 32, 64, 96, 104, 112, 120, 128 bits


from utils.bits import INT_MAX
from crypto.block.aes.aes import encrypt
import math
from pwn import xor


def inc(x_bytes):
    x = int.from_bytes(x_bytes, 'big')
    x = ((x >> 32) << 32) | (((x & INT_MAX) + 1) & INT_MAX)
    return x.to_bytes(16, 'big')


def mult(x_bytes, y_bytes):
    r = 0xe1 << 120  # 11100001 || 0*120
    x, y = int.from_bytes(x_bytes, 'big'), int.from_bytes(y_bytes, 'big')

    x = [1 if x & (1 << i) else 0 for i in range(127, -1, -1)]

    z0, v0 = 0, y
    for i in range(128):
        z1 = z0 ^ v0 if x[i] else z0
        v1 = (v0 >> 1) ^ r if v0 % 2 else v0 >> 1
        z0, v0 = z1, v1
    return z0.to_bytes(16, 'big')


def ghash(h, x):
    m = len(x) // 16
    x_blocks = [x[i * 16:(i + 1) * 16] for i in range(m)]
    y0 = b'\x00' * 16
    for i in range(m):
        y0 = mult(xor(y0, x_blocks[i]), h)
    return y0


def gctr(key, icb, x):
    if not x:
        return b''

    n = math.ceil(len(x) / 16)
    x_blocks = [x[i * 16:(i + 1) * 16] for i in range(n)]

    cbs = [icb]
    for i in range(1, n):
        cbs.append(inc(cbs[i - 1]))

    y_blocks = []
    for i in range(n):
        y_blocks.append(xor(x_blocks[i], encrypt(cbs[i], key)))
    return b''.join(y_blocks)


def encrypt_gcm(p, key, iv, aad, t_len):
    return crypt_helper(p, key, iv, aad, t_len, True)


def decrypt_gcm(c, key, iv, aad, t, t_len):
    p, t_act = crypt_helper(c, key, iv, aad, t_len, False)
    return p if t == t_act else None


def crypt_helper(data, key, iv, aad, t_len, enc):
    h = encrypt(b'\x00' * 16, key)

    iv_len = len(iv) * 8
    if iv_len == 96:
        iv += b'\x00\x00\x00\x01'
    else:
        s = 128 * math.ceil(iv_len / 128) - iv_len
        s_64 = b'\x00' * ((s + 64) // 8)
        iv_len_64 = int.to_bytes(iv_len, 8, 'big')
        iv = ghash(h, iv + s_64 + iv_len_64)

    data_out = gctr(key, inc(iv), data)

    data_len, aad_len = len(data) * 8, len(aad) * 8
    u = 128 * math.ceil(data_len / 128) - data_len
    v = 128 * math.ceil(aad_len / 128) - aad_len
    s = ghash(h, aad + b'\x00' * (v // 8)
              + (data_out if enc else data) + b'\x00' * (u // 8)
              + int.to_bytes(aad_len, 8, 'big')
              + int.to_bytes(data_len, 8, 'big'))

    t = gctr(key, iv, s)[:t_len // 8]

    return data_out, t


if __name__ == '__main__':
    from Crypto.Cipher import AES
    import random
    _key = random.randbytes(16)
    _iv = random.randbytes(12)
    _p = random.randbytes(128)
    _aad = random.randbytes(random.randrange(0, 1024))

    _c, _t = encrypt_gcm(_p, _key, _iv, _aad, 128)
    assert _p == decrypt_gcm(_c, _key, _iv, _aad, _t, 128)
    _t_len = random.randrange(1, 16) * 8
    assert _p == decrypt_gcm(_c, _key, _iv, _aad, _t[:_t_len // 8], _t_len)
    assert decrypt_gcm(_c, _key, _iv, _aad, _t[:-1] + b'?', 128) is None
    assert decrypt_gcm(_c, _key, _iv, _aad + b'?', _t, 128) is None

    _cipher = AES.new(_key, AES.MODE_GCM, nonce=_iv)
    _cipher.update(_aad)
    _c_act, _t_act = _cipher.encrypt_and_digest(_p)
    assert _c == _c_act
    assert _t == _t_act
