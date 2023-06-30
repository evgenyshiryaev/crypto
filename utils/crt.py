# https://e-maxx.ru/algo/chinese_theorem
# use sympy.ntheory.modular.crt()

import gmpy2


# Garner algo for chinese reminder theorem
def crt(a, p):
    x, r, mult = [], 0, 1
    for i in range(len(a)):
        x.append(a[i])
        for j in range(i):
            x[i] = gmpy2.divm(x[i] - x[j], p[j], p[i])
        r += x[i] * mult
        mult *= p[i]
    return r


if __name__ == '__main__':
    assert crt([69], [70]) == 69
    assert crt([1, 0], [17, 23]) == 69
