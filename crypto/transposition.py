import crypto.dictionary
import math
import random


def traspositionEncrypt(plainText, key):
    cipherText = ''
    for i in range(key):
        for j in range(i, len(plainText), key):
            cipherText += plainText[j]
    return cipherText


def traspositionDecrypt(cipherText, key):
    decryptKey = math.ceil(len(cipherText) / key)
    fullBlocks = len(cipherText) % key
    if fullBlocks == 0:
        fullBlocks = key
    # print(decryptKey, fullBlocks)

    plainText = ''
    for i in range(decryptKey):
        j = i
        count = 0
        for _ in range(key):
            if i == decryptKey - 1 and count == fullBlocks:
                break

            plainText += cipherText[j]
            # print(i, j, count, plainText)
            j += decryptKey
            if count >= fullBlocks:
                j -= 1
            count += 1
    return plainText


def getRandomKey(textLen):
    return random.randint(2, textLen)


def traspositionHack(cipherText, dictionaryPath, threshhold):
    dictionary = crypto.dictionary.load(dictionaryPath)
    for i in range(1, len(cipherText)):
        text = traspositionDecrypt(cipherText, i)
        if crypto.dictionary.analyse(text, dictionary) > threshhold:
            print('hack key =', i)
            print(text)


if __name__ == '__main__':
    plainText = 'Common sense is not so common.'
    key = getRandomKey(len(plainText))
    print(key)

    cipherText = traspositionEncrypt(plainText, key)
    print(cipherText)
    print(traspositionDecrypt(cipherText, key))

    traspositionHack(cipherText, '../../temp/words_alpha.txt', 0.95)
