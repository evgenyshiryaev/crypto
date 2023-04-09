import crypto.classic.dictionary
import math
import random


def encrypt(plain_text, key):
    cipher_text = ''
    for i in range(key):
        for j in range(i, len(plain_text), key):
            cipher_text += plain_text[j]
    return cipher_text


def decrypt(cipher_text, key):
    decrypt_key = math.ceil(len(cipher_text) / key)
    full_blocks = len(cipher_text) % key
    if full_blocks == 0:
        full_blocks = key
    # print(decrypt_key, full_blocks)

    plain_text = ''
    for i in range(decrypt_key):
        j = i
        count = 0
        for _ in range(key):
            if i == decrypt_key - 1 and count == full_blocks:
                break

            plain_text += cipher_text[j]
            # print(i, j, count, plain_text)
            j += decrypt_key
            if count >= full_blocks:
                j -= 1
            count += 1
    return plain_text


def get_random_key(text_len):
    return random.randint(2, text_len)


def hack(cipher_text, dictionary_path, threshold):
    dictionary = crypto.classic.dictionary.load(dictionary_path)
    for i in range(1, len(cipher_text)):
        text = decrypt(cipher_text, i)
        if crypto.classic.dictionary.analyse(text, dictionary) > threshold:
            print('hack key =', i)
            print(text)


if __name__ == '__main__':
    _plain_text = 'Common sense is not so common.'
    _key = get_random_key(len(_plain_text))
    print(_key)

    _cipher_text = encrypt(_plain_text, _key)
    print(_cipher_text)
    print(decrypt(_cipher_text, _key))

    hack(_cipher_text, '../../../temp/words_alpha.txt', 0.95)
