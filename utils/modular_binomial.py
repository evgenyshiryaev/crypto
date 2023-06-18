# https://www.ctfrecipes.com/cryptography/general-knowledge/maths/modular-arithmetic/modular-binomial

# N = p*q
# (a0*p + b0*q)**e0 = c0 mod N
# (a1*p + b1*q)**e1 = c1 mod N

# (a0*p)**e0*e1 + (b0*q)**e0*e1 = c0**e1 mod N
# (a1*p)**e0*e1 + (b1*q)**e0*e1 = c1**e0 mod N

# (a0*a1*p)**e0*e1 + (a1*b0*q)**e0*e1 = a1**e0*e1 * c0**e1 mod N
# (a0*a1*p)**e0*e1 + (a0*b1*q)**e0*e1 = a0**e0*e1 * c1**e0 mod N

import gmpy2


# b0 and b1 are not used
def modular_binomial(a0, c0, e0, a1, c1, e1, N):
    c = pow(a1, e0*e1, N) * pow(c0, e1, N) - pow(a0, e0*e1, N) * pow(c1, e0, N) % N
    q = int(gmpy2.gcd(c, N))
    return N // q, q


if __name__ == '__main__':
    from Crypto.Util.number import getPrime
    from random import randint
    _a0, _b0, _a1, _b1 = randint(1, 10), randint(1, 10), randint(1, 10), randint(1, 10)
    _e0, _e1 = randint(1, 100), randint(1, 100)
    _p, _q = getPrime(32), getPrime(32)
    _N = _p * _q
    _c0 = (_a0*_p + _b0*_q)**_e0 % _N
    _c1 = (_a1*_p + _b1*_q)**_e1 % _N

    assert _p, _q == modular_binomial(_a0, _c0, _e0, _a1, _c1, _e1, _N)
