def matrix_power(a, n, m):
    R = Integers(m)  # same as IntegerModRing
    M = Matrix(R, a)
    return M ^ n

_a = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
print(matrix_power(_a, 3, 100))
