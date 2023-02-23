import random
import string


DEFAULT_SYMBOLS = string.ascii_lowercase


def helper(plain_text, key, symbols, is_encrypt):
    cipher_text = ''
    for i in range(len(plain_text)):
        c = plain_text[i]
        s_i = symbols.find(c)
        k_i = symbols.find(key[i % len(key)])
        if not is_encrypt:
            k_i *= -1
        cipher_text += c if s_i == -1 else symbols[(s_i + k_i) % len(symbols)]
    return cipher_text


def encrypt(plain_text, key, symbols=DEFAULT_SYMBOLS):
    return helper(plain_text, key, symbols, False)


def decrypt(cipher_text, key, symbols=DEFAULT_SYMBOLS):
    return helper(cipher_text, key, symbols, True)


def get_random_key(key_len, symbols=DEFAULT_SYMBOLS):
    key = []
    for _ in range(key_len):
        i = random.randint(0, len(symbols) - 1)
        key.append(symbols[i])
    return ''.join(key)


if __name__ == '__main__':
    _plain_text = 'common sense is not so common'
    print(_plain_text)

    _key = get_random_key(5)
    print(_key)

    _cipher_text = encrypt(_plain_text, _key)
    print(_cipher_text)

    print(decrypt(_cipher_text, _key))
