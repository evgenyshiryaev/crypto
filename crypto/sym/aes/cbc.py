from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from pwn import *


key = get_random_bytes(16)
iv = get_random_bytes(16)


def encode(dec):
    return AES.new(key, AES.MODE_CBC, iv).encrypt(pad(dec, 16))


def is_padding_valid(enc):
    dec = AES.new(key, AES.MODE_CBC, iv).decrypt(enc)
    try:
        unpad(dec, 16)
    except ValueError:
        return False
    return True


def padding_oracle_hack(enc):
    dec = b''

    blocks = len(enc) // 16

    for block_i in range(blocks - 2, -1, -1):
        enc1 = list(enc)
        block_key = [0] * 16

        for b_i in range(15, -1, -1):
            pad_len = 16 - b_i
            i = 16 * block_i + b_i

            for j in range(1, pad_len):
                enc1[i + j] = block_key[16 - pad_len + j] ^ pad_len

            found = False
            for b in range(256):
                if b == enc[i]:
                    continue
                enc1[i] = b
                if is_padding_valid(bytes(enc1[:len(enc1) - 16 * (blocks - 2 - block_i)])):
                    found = True
                    break
            if not found:
                b = enc[i]

            block_key[b_i] = b ^ pad_len
            dec = (enc[i] ^ block_key[b_i]).to_bytes(1, 'little') + dec

    return dec


if __name__ == '__main__':
    _text = b'Nobody can decrypt this even with is_padding_valid function'
    _enc = encode(_text)
    print(padding_oracle_hack(_enc))
