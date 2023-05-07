import re
import string

BASE_64_SYMBOLS = string.ascii_uppercase + string.ascii_lowercase + string.digits + '+/'


def base64_encode(plain_text):
    plain_text_bytes = plain_text.encode()
    i = 0
    bit = 1 << 7  # high bit in byte
    padding = 0
    cipher_text = ''

    while i < len(plain_text_bytes) - 1 or bit != 0:
        c = 0
        for _ in range(6):
            if bit == 0:
                if i < len(plain_text_bytes) - 1:
                    i += 1
                    bit = 1 << 7
                else:
                    padding += 1

            b = 1 if bit > 0 and (plain_text_bytes[i] & bit) != 0 else 0
            c = (c << 1) + b
            bit >>= 1

        cipher_text += BASE_64_SYMBOLS[c]

    for _ in range(padding // 2):
        cipher_text += '='

    return cipher_text


def base64_decode(cipher_text):
    cipher_text = re.compile('\s').sub('', cipher_text)
    i = 0
    cipher_text_byte = BASE_64_SYMBOLS.find(cipher_text[i])
    bit = 1 << 5  # high bit in base64 symbol
    plain_text = bytearray()

    while i < len(cipher_text) - 1:
        c = 0
        for _ in range(8):
            if bit == 0:
                i += 1
                while cipher_text[i].isspace():
                    i += 1
                cipher_text_byte = BASE_64_SYMBOLS.find(cipher_text[i]) if cipher_text[i] != '=' else 0
                bit = 1 << 5

            b = 1 if bit > 0 and (cipher_text_byte & bit) != 0 else 0
            c = (c << 1) + b
            bit >>= 1

        plain_text.append(c)

    return plain_text.decode()


if __name__ == '__main__':
    _plain_text = 'abc'
    print(_plain_text)

    _cipher_text = base64_encode(_plain_text)
    print(_cipher_text)

    print(base64_decode(_cipher_text))
