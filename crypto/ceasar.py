import crypto.dictionary
import random
import string
import utils.euclid

DEFAULT_SYMBOLS = string.ascii_letters + string.digits

def ceaserHelper(plainText, f, symbols):
    cipherText = ''
    for c in plainText:
        i = symbols.find(c)
        cipherText += c if i == -1 else symbols[f(i)]
    return cipherText


def ceaserEncrypt(plainText, key, symbols = DEFAULT_SYMBOLS):
    return affineEncrypt(plainText, 1, key, symbols)

def ceaserDecrypt(cipherText, key, symbols = DEFAULT_SYMBOLS):
    return affineDecrypt(cipherText, 1, key, symbols)


def multiplicativeEncrypt(plainText, key, symbols = DEFAULT_SYMBOLS):
    return affineEncrypt(plainText, key, 0, symbols)

def multiplicativeDecrypt(cipherText, key, symbols = DEFAULT_SYMBOLS):
    return affineDecrypt(cipherText, key, 0, symbols)


def affineEncrypt(plainText, keyMult, keyAdd, symbols = DEFAULT_SYMBOLS):
    d = utils.euclid.gcd(keyMult, len(symbols))
    if d != 1: raise Exception
    return ceaserHelper(plainText, lambda a : (a * keyMult + keyAdd) % len(symbols), symbols)

def affineDecrypt(cipherText, keyMult, keyAdd, symbols = DEFAULT_SYMBOLS):
    d = utils.euclid.gcd(keyMult, len(symbols))
    if d != 1: raise Exception
    return ceaserHelper(cipherText,
            lambda a : utils.euclid.divMod(a - keyAdd, keyMult, len(symbols)), symbols)


def getRandomKeys(symbols = DEFAULT_SYMBOLS):
    keyAdd = random.randint(1, len(symbols) - 1)
    while True:
        keyMult = random.randint(2, len(symbols) - 1)
        if utils.euclid.gcd(keyMult, len(symbols)) == 1: return keyMult, keyAdd


def affineHack(cipherText, symbols, dictionaryPath, threshhold):
    dictionary = crypto.dictionary.load(dictionaryPath)
    for keyMult in range(1, len(symbols)):
        if utils.euclid.gcd(keyMult, len(symbols)) != 1:
            continue
        for keyAdd in range(0, len(symbols)):
            text = affineDecrypt(cipherText, keyMult, keyAdd, symbols)
            if crypto.dictionary.analyse(text, dictionary) > threshhold:
                print('hack keys =', keyMult, keyAdd)
                print(text)


if __name__ == '__main__':
    plainText = 'This is secret abc'
    keyMult, keyAdd = getRandomKeys()
    print('Keys =', keyMult, keyAdd)

    cipherText = ceaserEncrypt(plainText, keyAdd)
    print(cipherText)
    print(ceaserDecrypt(cipherText, keyAdd))

    cipherText = multiplicativeEncrypt(plainText, keyMult)
    print(cipherText)
    print(multiplicativeDecrypt(cipherText, keyMult))

    cipherText = affineEncrypt(plainText, keyMult, keyAdd)
    print(cipherText)
    print(affineDecrypt(cipherText, keyMult, keyAdd))

    for i in range(2, 100):
        if utils.euclid.gcd(i, len(DEFAULT_SYMBOLS)) == 1:
            cipherText = multiplicativeEncrypt(plainText, i)
            if cipherText == plainText:
                print('Dup mult key =', i)
                break

    cipherText = affineEncrypt(plainText, keyMult, keyAdd)
    print(cipherText)
    affineHack(cipherText, DEFAULT_SYMBOLS, '../../temp/words_alpha.txt', 0.95)
