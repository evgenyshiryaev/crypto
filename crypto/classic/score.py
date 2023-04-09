import string


SYMS = string.ascii_lowercase
FREQ = 'etaoinshrdlcumwfgypbvkjxqz'


def get_letter_count(text):
    letter_count = {}
    for c in SYMS:
        letter_count[c] = 0
    for c in text.lower():
        if c in letter_count:
            letter_count[c] += 1
    return letter_count


def get_freq(text):
    letter_count = get_letter_count(text)

    freq = {}
    for c in SYMS:
        f = letter_count[c]
        if f not in freq:
            freq[f] = []
        freq[f].append(c)

    for f in freq:
        freq[f].sort(key=FREQ.find, reverse=True)
        freq[f] = ''.join(freq[f])

    freq = list(freq.items())
    freq.sort(key=lambda a: a[0], reverse=True)

    freq = list(map(lambda a: a[1], freq))

    return ''.join(freq)


def get_freq_score(text):
    freq = get_freq(text)

    score = 0
    for c in FREQ[:6]:
        if c in freq[:6]:
            score += 1
    for c in FREQ[-6:]:
        if c in freq[:-6]:
            score += 1
    return score


if __name__ == '__main__':
    _text = '''Cryptography is the study of secure communications techniques that allow only the sender and
        intended recipient of a message to view its contents. The term is derived from the Greek word kryptos,
        which means hidden. It is closely associated to encryption, which is the act of scrambling ordinary text
        into what's known as ciphertext and then back again upon arrival. In addition, cryptography also covers
        the obfuscation of information in images using techniques such as microdots or merging. Ancient Egyptians
        were known to use these methods in complex hieroglyphics, and Roman Emperor Julius Caesar is credited
        with using one of the first modern ciphers.'''

    _letter_count = get_letter_count(_text)
    print(_letter_count)

    _freq = get_freq(_text)
    print(_freq)

    _score = get_freq_score(_text)
    print(_score)
