import gmpy2


def encrypt(p, q, m):
    assert gmpy2.is_prime(p)
    assert gmpy2.is_prime(q)
    assert p % 4 == 3
    assert q % 4 == 3
    return gmpy2.powmod(m, 2, p * q)


def decrypt(p, q, m):
    r = gmpy2.powmod(m, (p + 1) // 4, p)
    s = gmpy2.powmod(m, (q + 1) // 4, q)
    n = p * q

    (_, a, b) = gmpy2.gcdext(p, q)

    x0 = (a * p * s + b * q * r) % n
    x1 = n - x0
    y0 = (a * p * s - b * q * r) % n
    y1 = n - y0

    return int(x0), int(x1), int(y0), int(y1)


if __name__ == '__main__':
    _p = 861346721469213227608792923571
    _q = 1157379696919172022755244871343
    _m = 1234124102741927349127340917294387
    print(_m)

    _enc = encrypt(_p, _q, _m)
    print(_enc)

    _dec = decrypt(_p, _q, _enc)
    print(_dec)
    assert _m in _dec
