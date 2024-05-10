import numpy as np

# a ^ n % m
# numpy.linalg.matrix_power with module
def matrix_power(a, n, m):
    if n == 0:
        return 1
    y = np.identity(len(a), dtype=np.integer)
    while n > 1:
        if n & 1:
            y = np.matmul(a, y) % m
        a = np.matmul(a, a) % m
        n >>= 1
    return np.matmul(a, y) % m


if __name__ == '__main__':
    _a = np.arange(9).reshape(3, 3)
    print(_a)
    print(np.linalg.matrix_power(_a, 3))
    print(matrix_power(_a, 3, 100))
