import crypto.dictionary
import random
import re
import string


DEFAULT_SYMBOLS = string.ascii_lowercase


def substitutionEncrypt(plainText, symbols, key, validateKey = True):
    if validateKey and not isKeyValue(symbols, key): raise Exception

    plainText = plainText.lower()
    cipherText = ''
    for c in plainText:
        if not c in symbols and c in key and not validateKey:
            cipherText += '_'
        else:
            cipherText += key[symbols.find(c)] if c in symbols else c
    return cipherText


def substitutionDecrypt(cipherText, symbols, key, validateKey = True):
    return substitutionEncrypt(cipherText, key, symbols, validateKey)


def isKeyValue(symbols, key):
    s = list(symbols)
    k = list(key)
    s.sort()
    k.sort()
    return s == k


def getRandomKey(symbols):
    key = list(symbols)
    random.shuffle(key)
    return ''.join(key)


def substitutionHack(cipherText, symbols, dictionaryPath):
    mapping = {}
    for c in symbols: mapping[c] = set()
    patterns = crypto.dictionary.loadPatterns(dictionaryPath)

    for word in re.compile('[^a-z\s]').sub('', cipherText.lower()).split():
        wordMapping = {}
        for c in symbols: wordMapping[c] = set()

        wordPattern = crypto.dictionary.getPattern(word)
        if not wordPattern in patterns: continue

        for candidate in patterns[wordPattern]:
            for i in range(len(word)):
                wordMapping[word[i]].add(candidate[i])

        for c in symbols:
            if len(mapping[c]) == 0:
                mapping[c] = wordMapping[c]
            elif wordMapping[c]:
                mapping[c] &= wordMapping[c]
                if len(mapping[c]) == 0: raise Exception

    print(mapping)

    key = ['_'] * len(symbols)
    for k, v in mapping.items():
        if len(v) == 1:
            c = list(v)[0]
            key[symbols.find(c)] = k
    key = ''.join(key)
    print(key)

    plainText = substitutionDecrypt(cipherText, symbols, key, False)
    print(plainText)


if __name__ == '__main__':
    plainText = 'Common sense is not so common incredible impedance electrochemical impedance spectroscopy nondeterministic.'

    key = getRandomKey(DEFAULT_SYMBOLS)
    print(DEFAULT_SYMBOLS)
    print(key)

    cipherText = substitutionEncrypt(plainText, DEFAULT_SYMBOLS, key)
    print(cipherText)

    print(substitutionDecrypt(cipherText, DEFAULT_SYMBOLS, key))

    substitutionHack(cipherText, DEFAULT_SYMBOLS, '../../temp/words_alpha.txt')
