# https://e-maxx.ru/algo/chinese_theorem

import gmpy2


def solve(a, p):
    x = []
    r = 0
    mult = 1

    for i in range(len(a)):
        x.append(a[i])
        for j in range(i):
            x[i] = gmpy2.divm(x[i] - x[j], p[j], p[i])

        r += x[i] * mult
        mult *= p[i]

    return r


if __name__ == "__main__":
    print(solve([69], [70]))  # 69
    print(solve([1, 0], [17, 23]))  # 69
