# see http://quipqiup.com/

import string


def load(path):
    with open(path) as dictionary:
        return set(dictionary.read().split())


def analyse(text, dictionary):
    in_dictionary = 0
    total = 0

    for word in text.split():
        word = word.strip(string.punctuation).lower()
        if word in dictionary:
            in_dictionary += 1
        total += 1

    return in_dictionary / total


# {'0': ['a'], '0.0': ['aa'], '0.0.1': ['aah', 'aal']}
def load_patterns(path):
    patterns = {}
    with open(path) as dictionary:
        for word in dictionary.read().split():
            pattern = get_pattern(word)
            if not pattern in patterns:
                patterns[pattern] = []
            patterns[pattern].append(word)
    return patterns


def get_pattern(word):
    index = 0
    chars = {}
    pattern = []
    for char in word:
        if not char in chars:
            chars[char] = str(index)
            index += 1
        pattern.append(chars[char])
    return '.'.join(pattern)


if __name__ == '__main__':
    _path = '../../../../temp/words_alpha.txt'

    _dictionary = load(_path)
    # print(dictionary)
    assert('fate' in _dictionary)
    assert('nofate' not in _dictionary)

    print(analyse('This is biiiiig secret orno', _dictionary))

    _patterns = load_patterns(_path)
    # print(patterns)
    print(_patterns['0.1.2.3.4.5.6.7.8.9.10.11.12.13'])
