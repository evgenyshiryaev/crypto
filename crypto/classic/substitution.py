import crypto.classic.dictionary
import random
import re
import string


DEFAULT_SYMBOLS = string.ascii_lowercase


def encrypt(plain_text, symbols, key, validate_key=True):
    assert(not validate_key or is_key_valid(symbols, key))

    plain_text = plain_text.lower()
    cipher_text = ''
    for c in plain_text:
        if not c in symbols and c in key and not validate_key:
            cipher_text += '_'
        else:
            cipher_text += key[symbols.find(c)] if c in symbols else c
    return cipher_text


def decrypt(cipher_text, symbols, key, validate_key=True):
    return encrypt(cipher_text, key, symbols, validate_key)


def is_key_valid(symbols, key):
    s = list(symbols)
    k = list(key)
    s.sort()
    k.sort()
    return s == k


def get_random_key(symbols):
    key = list(symbols)
    random.shuffle(key)
    return ''.join(key)


def hack(cipher_text, symbols, dictionary_path):
    mapping = {}
    for c in symbols:
        mapping[c] = set()
    patterns = crypto.classic.dictionary.load_patterns(dictionary_path)

    for word in re.compile('[^a-z\s]').sub('', cipher_text.lower()).split():
        word_mapping = {}
        for c in symbols:
            word_mapping[c] = set()

        word_pattern = crypto.classic.dictionary.get_pattern(word)
        if not word_pattern in patterns:
            continue

        for candidate in patterns[word_pattern]:
            for i in range(len(word)):
                word_mapping[word[i]].add(candidate[i])

        for c in symbols:
            if len(mapping[c]) == 0:
                mapping[c] = word_mapping[c]
            elif word_mapping[c]:
                mapping[c] &= word_mapping[c]
                if len(mapping[c]) == 0:
                    raise Exception

    print(mapping)

    key = ['_'] * len(symbols)
    for k, v in mapping.items():
        if len(v) == 1:
            c = list(v)[0]
            key[symbols.find(c)] = k
    key = ''.join(key)
    print(key)

    plain_text = decrypt(cipher_text, symbols, key, False)
    print(plain_text)


if __name__ == '__main__':
    _plain_text = 'Common sense is not so common incredible impedance electrochemical impedance spectroscopy nondeterministic.'

    _key = get_random_key(DEFAULT_SYMBOLS)
    print(DEFAULT_SYMBOLS)
    print(_key)

    _cipher_text = encrypt(_plain_text, DEFAULT_SYMBOLS, _key)
    print(_cipher_text)

    print(decrypt(_cipher_text, DEFAULT_SYMBOLS, _key))

    hack(_cipher_text, DEFAULT_SYMBOLS, '../../../temp/words_alpha.txt')
