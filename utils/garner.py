import utils.euclid


def garnerSolve(a, p):
    x = []
    r = 0
    pMult = 1

    for i in range(len(a)):
        x.append(a[i])
        for j in range(i):
            x[i] = utils.euclid.divMod(x[i] - x[j], p[j], p[i])

        r += x[i] * pMult
        pMult *= p[i]

    return r


if __name__ == "__main__":
    print(garnerSolve([69], [70])) # 69
    print(garnerSolve([1, 0], [17, 23])) # 69
