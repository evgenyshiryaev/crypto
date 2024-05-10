# https://github.com/miekrr/HashPump

# secret_len is known
# secret is unknown
# hash(secret) is known


import crypto.hash.md5
import hashlib
import random


secret_len = random.randrange(1, 1000000)
secret = random.randbytes(secret_len)


def md5_length_extension():
    secret_md5 = hashlib.md5(secret).digest()
    attack = random.randbytes(random.randint(1, 1000000))
    suffix = crypto.hash.md5.md5.padding(secret_len) + attack

    data_md5 = crypto.hash.md5.md5.digest(attack, secret_md5, secret_len)
    assert data_md5 == hashlib.md5(secret + suffix).digest()


if __name__ == '__main__':
    md5_length_extension()
