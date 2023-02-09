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
def loadPatterns(path):
    patterns = {}
    with open(path) as dictionary:
        for word in dictionary.read().split():
            pattern = getPattern(word)
            if not pattern in patterns: patterns[pattern] = []
            patterns[pattern].append(word)
    return patterns


def getPattern(word):
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
    path = '../../temp/words_alpha.txt'

    dictionary = load(path)
    # print(dictionary)
    print('fate' in dictionary)
    print('nofate' in dictionary)

    print(analyse('This is biiiiig secret orno', dictionary))

    patterns = loadPatterns(path)
    # print(patterns)
    print(patterns['0.1.2.3.4.5.6.7.8.9.10.11.12.13'])
