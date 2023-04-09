from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from pwn import *


key = get_random_bytes(16)
nonce = get_random_bytes(8)


def encode_decode(text):
    enc0 = b''
    counter = 0
    cipher = AES.new(key, AES.MODE_ECB)
    for i in range(0, len(text), 16):
        block_key = cipher.encrypt(nonce + counter.to_bytes(8, 'big'))
        counter += 1
        block = text[i: i + 16]
        enc0 += xor(block, block_key[: len(block)])

    enc1 = AES.new(key, AES.MODE_CTR, nonce=nonce).encrypt(text)
    assert enc0 == enc1

    dec = b''
    counter = 0
    for i in range(0, len(enc0), 16):
        block_key = cipher.encrypt(nonce + counter.to_bytes(8, 'big'))
        counter += 1
        block = enc0[i: i + 16]
        dec += xor(block, block_key[: len(block)])
    assert text == dec


if __name__ == '__main__':
    _text = b'12345 some text to encrypt and decrypt'
    encode_decode(_text)
