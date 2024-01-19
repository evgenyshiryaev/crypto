from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from pwn import *
import string


key = get_random_bytes(16)
cipher = AES.new(key, AES.MODE_ECB)

hack_postfix = b64d('Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK')


def hack_encrypt(prefix):
    return cipher.encrypt(pad(prefix + hack_postfix, AES.block_size))


def hack():
    r_len = len(hack_encrypt(b''))
    r = b''

    for i in range(r_len):
        block_count = i // 16 + 1
        block0 = (b'\x00' * max(0, 15 - len(r))) + r[-15:]
        block1 = b'\x00' * (15 - len(r) % 16)
        for c in string.printable:
            b = c.encode()
            dec = block0 + b + block1
            enc = hack_encrypt(dec)
            if enc[:16] == enc[16 * block_count: 16 * block_count + 16]:
                r += b
                break
    return r


def profile_for(email):
    assert '&' not in email
    assert '=' not in email
    profile = f'email={email}&uid=10&role=user'
    return cipher.encrypt(pad(profile.encode(), AES.block_size))


def dec_profile(profile_enc):
    profile = unpad(cipher.decrypt(profile_enc), AES.block_size).decode()
    r = {}
    for pair in profile.split('&'):
        vals = pair.split('=')
        r[vals[0]] = vals[1]
    return r


def hack_profile_for():
    email = '\x00' * 16 + 'admin'
    email = pad(email.encode(), 16)[6:].decode()
    enc0 = profile_for(email)

    email = '\x00' * 13
    enc1 = profile_for(email)

    enc = enc1[:32] + enc0[16:32]
    return dec_profile(enc)


if __name__ == '__main__':
    print(hack())

    _profile_enc = profile_for('test@test.ru')
    print(dec_profile(_profile_enc))
    print(hack_profile_for())
