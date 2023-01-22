import string


def ceaserEncrypt(plainText, key, symbols = string.ascii_letters + string.digits):
    cipherText = ''
    for c in plainText:
        plainPos = symbols.find(c)
        if plainPos == -1:
            cipherText += c
        else:
            cipherPos = (plainPos + key) % len(symbols)
            cipherText += symbols[cipherPos]
    return cipherText


def ceaserDecrypt(cipherText, key, symbols = string.ascii_letters + string.digits):
    return ceaserEncrypt(cipherText, -key, symbols)


# print(ceaserEncrypt('This is secret', 69))
# print(ceaserDecrypt(ceaserEncrypt('This is secret', 69), 69))
