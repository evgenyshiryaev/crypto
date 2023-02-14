PLAIN_TO_CIPHER = {
    'a' : '.-', 'b' : '-...', 'c' : '-.-.', 'd' : '-..', 'e' : '.', 'f' : '..-.',
    'g' : '--.', 'h' : '....', 'i' : '..', 'j' : '.---', 'k' : '-.-', 'l' : '.-..',
    'm' : '--', 'n' : '-.', 'o' : '---', 'p' : '.--.', 'q' : '--.-', 'r' : '.-.', 's' : '...',
    't' : '-', 'u': '..-', 'v' : '...-', 'w' : '.--', 'x' : '-..-', 'y' : '-.--', 'z' : '--..',
    '1' : '.----', '2' : '..---', '3' : '...--', '4' : '....-', '5' : '.....',
    '6' : '-....', '7' : '--...', '8' : '---..', '9' : '----.', '0' : '-----'
    }

CIPHER_TO_PLAIN = {}
for _p, _c in PLAIN_TO_CIPHER.items():
    CIPHER_TO_PLAIN[_c] = _p


def encrypt(plain_text, key='.-'):
    cipher_text = ''
    for c in plain_text.lower():
        if c in PLAIN_TO_CIPHER:
            cipher_text += PLAIN_TO_CIPHER[c].replace('.', key[0]).replace('-', key[1])
            cipher_text += ' '
    return cipher_text


def decrypt(cipher_text, key='.-'):
    plain_text = ''
    for c in cipher_text.split():
        c = c.replace(key[0], '.').replace(key[1], '-')
        if c in CIPHER_TO_PLAIN:
            plain_text += CIPHER_TO_PLAIN[c]
        else:
            print('Unknown ' + c)
    return plain_text


if __name__ == '__main__':
    print(encrypt('This is secret'))
    print(decrypt(encrypt('This is secret')))

    print(encrypt('This is secret', '%A'))
    print(decrypt(encrypt('This is secret', '%A'), '%A'))
