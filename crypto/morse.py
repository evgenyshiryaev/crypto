morsePlainToCipher = {
    'a' : '.-', 'b' : '-...', 'c' : '-.-.', 'd' : '-..', 'e' : '.', 'f' : '..-.',
    'g' : '--.', 'h' : '....', 'i' : '..', 'j' : '.---', 'k' : '-.-', 'l' : '.-..',
    'm' : '--', 'n' : '-.', 'o' : '---', 'p' : '.--.', 'q' : '--.-', 'r' : '.-.', 's' : '...',
    't' : '-', 'u': '..-', 'v' : '...-', 'w' : '.--', 'x' : '-..-', 'y' : '-.--', 'z' : '--..',
    '1' : '.----', '2' : '..---', '3' : '...--', '4' : '....-', '5' : '.....',
    '6' : '-....', '7' : '--...', '8' : '---..', '9' : '----.', '0' : '-----'
    }

morseCipherToPlain = {}
for p, c in morsePlainToCipher.items():
    morseCipherToPlain[c] = p


def morseEncrypt(plainText, key = '.-'):
    cipherText = ''
    for c in plainText.lower():
        if c in morsePlainToCipher:
            cipherText += morsePlainToCipher[c].replace('.', key[0]).replace('-', key[1])
            cipherText += ' '
    return cipherText


def morseDecrypt(cipherText, key = '.-'):
    plainText = ''
    for c in cipherText.split():
        c = c.replace(key[0], '.').replace(key[1], '-')
        if c in morseCipherToPlain:
            plainText += morseCipherToPlain[c]
        else:
            print('Unknown ' + c)
    return plainText


if __name__ == '__main__':
    print(morseEncrypt('This is secret'))
    print(morseDecrypt(morseEncrypt('This is secret')))

    print(morseEncrypt('This is secret', '%A'))
    print(morseDecrypt(morseEncrypt('This is secret', '%A'), '%A'))
