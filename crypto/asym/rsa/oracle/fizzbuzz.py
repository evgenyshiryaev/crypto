# https://2023.cor.team/challs
# https://7rocky.github.io/en/ctf/other/corctf/fizzbuzz101/


def oracle(m, n, div):
    return (m % n) % div != 0


# m % div == 0

# increase k0 until k0*m % div != 0
# (k0-1)*m < n < k0*m
# n//k0 <= m <= n//(k0-1)

# div*(k0-1)*m < div*n < div*k0*m
# increase k1 > div*(k0-1) until k1*m % div == 0
# k*m > div*n
# div*n//k1 <= m <= div*n//(k1-1)


def binary_search(l, r, m, n, div, reverse=False):
    while l < r - 1:
        mid = (l + r) // 2
        if oracle(m * mid, n, div) ^ reverse:
            r = mid
        else:
            l = mid
    return l, r


def hack(m, n, div):
    # exponential search
    k = 2
    while not oracle(m * k, n, div):
        k *= 2
    l, r = binary_search(k // 2, k, m, n, div)
    # print(l, r)
    # print(n // r)
    # print(n // (r - 1))

    i = 1
    while True:
        l, r = binary_search(div * l, div * r, m, n, div, True)
        # print(div ** i * n // r)
        # print(div ** i * n // (r - 1))
        if div ** i * n // r + 1 >= div ** i * n // (r - 1):
            break
        i += 1
    return div ** i * n // (r - 1)



if __name__ == '__main__':
    from crypto.asym.rsa.rsa import generate_key
    import random

    _BITS = 512
    _, _, _n = generate_key(_BITS)

    _DIV = 5  # any
    while True:
        _m = random.randrange(1, _n)
        if not oracle(_m, _n, _DIV) and not oracle(2 * _m, _n, _DIV):
            break

    assert _m == hack(_m, _n, _DIV)
