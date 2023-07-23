# https://en.wikipedia.org/wiki/Carmichael_number

from gmpy2 import gcd
import random


# false-positive for Carmichael numbers
def fermat(n):
    for a in range(2, n):
        if not fermat_a(a, n):
            return False
    return True


def fermat_a(a, n):
    return pow(a, n, n) == a


def miller_rabin(n, fail_chance=0.0001):
    fc, aset = 1.0, set()
    while fc > fail_chance:
        a = random.randrange(2, n)
        if a in aset:
            continue
        if not miller_rabin_a(a, n):
            return False
        fc *= .25
        aset.add(a)
    return True


def miller_rabin_a(a, n):
    if n & 1 == 0 or gcd(a, n) > 1:
        return False
    q, k = n - 1, 0
    while q & 1 == 0:
        q, k = q >> 1, k + 1
    a = pow(a, q, n)
    if a == 1:
        return True
    for i in range(k):
        if a == -1 % n:
            return True
        a = pow(a, 2, n)
    return False


if __name__ == '__main__':
    # 561 = 3 * 11 * 17  - Carmichael number
    _ns = (13, 15, 561)
    assert all([fermat(_ns[0]), not fermat(_ns[1]), fermat(_ns[2])])
    assert all([miller_rabin(_ns[0]), not miller_rabin(_ns[1]), not miller_rabin(_ns[2])])
