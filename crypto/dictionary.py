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


if __name__ == '__main__':
    dictionary = load('../../temp/words_alpha.txt')
    print('fate' in dictionary)
    print('nofate' in dictionary)

    print(analyse('This is biiiiig secret orno', dictionary))
