import crypto.classic.dictionary
import gmpy2
import random
import string


DEFAULT_SYMBOLS = string.ascii_lowercase


def helper(plain_text, f, symbols):
    cipher_text = ''
    for c in plain_text:
        i = symbols.find(c)
        cipher_text += c if i == -1 else symbols[f(i)]
    return cipher_text


def ceaser_encrypt(plain_text, key, symbols=DEFAULT_SYMBOLS):
    return affine_encrypt(plain_text, 1, key, symbols)


def ceaser_decrypt(cipher_text, key, symbols=DEFAULT_SYMBOLS):
    return affine_decrypt(cipher_text, 1, key, symbols)


def multiplicative_encrypt(plain_text, key, symbols=DEFAULT_SYMBOLS):
    return affine_encrypt(plain_text, key, 0, symbols)


def multiplicative_decrypt(cipher_text, key, symbols=DEFAULT_SYMBOLS):
    return affine_decrypt(cipher_text, key, 0, symbols)


def affine_encrypt(plain_text, key_mult, key_add, symbols=DEFAULT_SYMBOLS):
    d = gmpy2.gcd(key_mult, len(symbols))
    assert d == 1
    return helper(plain_text, lambda a: (a * key_mult + key_add) % len(symbols), symbols)


def affine_decrypt(cipher_text, key_mult, key_add, symbols=DEFAULT_SYMBOLS):
    d = gmpy2.gcd(key_mult, len(symbols))
    assert d == 1
    return helper(cipher_text, lambda a: gmpy2.divm(a - key_add, key_mult, len(symbols)), symbols)


def get_random_keys(symbols=DEFAULT_SYMBOLS):
    key_add = random.randint(1, len(symbols) - 1)
    while True:
        key_mult = random.randint(2, len(symbols) - 1)
        if gmpy2.gcd(key_mult, len(symbols)) == 1:
            return key_mult, key_add


def affine_hack(cipher_text, symbols, dictionary_path, threshold):
    dictionary = crypto.classic.dictionary.load(dictionary_path)
    for key_mult in range(1, len(symbols)):
        if gmpy2.gcd(key_mult, len(symbols)) != 1:
            continue
        for key_add in range(0, len(symbols)):
            text = affine_decrypt(cipher_text, key_mult, key_add, symbols)
            if crypto.classic.dictionary.analyse(text, dictionary) > threshold:
                print('hack keys =', key_mult, key_add)
                print(text)


if __name__ == '__main__':
    _plain_text = 'this is secret abc'
    _key_mult, _key_add = get_random_keys()
    print('Keys =', _key_mult, _key_add)

    _cipher_text = ceaser_encrypt(_plain_text, _key_add)
    print(_cipher_text)
    print(ceaser_decrypt(_cipher_text, _key_add))

    _cipher_text = multiplicative_encrypt(_plain_text, _key_mult)
    print(_cipher_text)
    print(multiplicative_decrypt(_cipher_text, _key_mult))

    _cipher_text = affine_encrypt(_plain_text, _key_mult, _key_add)
    print(_cipher_text)
    print(affine_decrypt(_cipher_text, _key_mult, _key_add))

    for _i in range(2, 100):
        if gmpy2.gcd(_i, len(DEFAULT_SYMBOLS)) == 1:
            _cipher_text = multiplicative_encrypt(_plain_text, _i)
            if _cipher_text == _plain_text:
                print('Dup mult key =', _i)
                break

    _cipher_text = affine_encrypt(_plain_text, _key_mult, _key_add)
    print(_cipher_text)
    affine_hack(_cipher_text, DEFAULT_SYMBOLS, '../../../temp/words_alpha.txt', 0.95)
