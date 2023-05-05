# https://e-maxx.ru/algo/linear_systems_gauss

# Ax = B
# Ax == B mod q
# A: Y * X (m * n)
# x: X * 1
# B: Y * 1


import gmpy2
import numpy as np


def gauss_jordan(a, b):
    Y, X = a.shape  # m, n

    ab = np.zeros(shape=(Y, X + 1))
    ab[:, :X] = a
    ab[:, X] = b

    outer_loop = [[0, Y - 1, 1], [Y - 1, 0, -1]]

    for d in range(2):
        for i in range(outer_loop[d][0], outer_loop[d][1], outer_loop[d][2]):
            inner_loop = [[i + 1, Y, 1], [i - 1, -1, -1]]
            for j in range(inner_loop[d][0], inner_loop[d][1], inner_loop[d][2]):
                k = (-1) * ab[j, i] / ab[i, i]
                temp_row = ab[i, :] * k
                ab[j, :] = ab[j, :] + temp_row

    for i in range(Y):
        ab[i, :] = ab[i, :] / ab[i, i]

    return ab[:, X]


def gauss_jordan_mod(a, b, q):
    Y, X = a.shape  # m, n

    ab = np.zeros(shape=(Y, X + 1), dtype=np.int64)
    ab[:, :X] = a
    ab[:, X] = b

    outer_loop = [[0, Y - 1, 1], [Y - 1, 0, -1]]

    for d in range(2):
        for i in range(outer_loop[d][0], outer_loop[d][1], outer_loop[d][2]):
            inner_loop = [[i + 1, Y, 1], [i - 1, -1, -1]]
            for j in range(inner_loop[d][0], inner_loop[d][1], inner_loop[d][2]):
                k = (-1) * ab[j, i] * gmpy2.invert(int(ab[i, i]), q)
                temp_row = ab[i, :] * k
                ab[j, :] = (ab[j, :] + temp_row) % q

    for i in range(Y):
        ab[i, :] = (ab[i, :] * gmpy2.invert(int(ab[i, i]), q)) % q

    return ab[:, X]


if __name__ == '__main__':
    import random
    _q = 13
    _y = 4
    _x = 4
    A = np.matrix([[random.randint(0, _q - 1) for _ in range(_x)] for _ in range(_y)])
    s = np.matrix([random.randint(0, _q - 1) for _ in range(_x)])

    B = A * s.transpose()
    print(gauss_jordan(A, B.transpose()))

    B = (A * s.transpose()) % _q
    print(gauss_jordan_mod(A, B.transpose(), _q))
