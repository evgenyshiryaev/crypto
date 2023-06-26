# https://cryptobook.nakov.com/digital-signatures/ecdsa-sign-verify-messages
# https://en.wikipedia.org/wiki/Elliptic_Curve_Digital_Signature_Algorithm

from crypto.ec.ec_weierstrass import WeierstrassCurve, WeierstrassPoint
import gmpy2
import random


# non-ec dsa, just for example
# n - order
# p - prime
# x - base point
# d - private key
# q = (x*d)%p - public key
def sign_non_ec(n, p, x, d, h):
    while True:
        k = random.randrange(1, n - 1)
        x1 = (x * k) % p
        r = x1 % n
        if r == 0:
            continue
        s = (gmpy2.invert(k, n) * (h + r * d)) % n
        if s == 0:
            continue
        return r, s


def verify_non_ec(n, p, x, q, h, r, s):
    if not (1 <= r <= n - 1) or not (1 <= s <= n - 1):
        return False
    w = gmpy2.invert(s, n)
    u1, u2 = (h * w) % n, (r * w) % n
    x2 = (u1 * x + u2 * q) % p
    return x2 != 0 and x2 % n == r


# ec dsa
# n - order
# p - prime
# a, b - curve params
# (x, y) - base point
# d - private key
# (qx, qy) - public key
def sign(n, p, a, b, x, y, d, h, leak_k=False):
    curve = WeierstrassCurve(p, a, b)
    g = WeierstrassPoint(curve, x, y)
    while True:
        k = random.randrange(1, n)
        x1 = (g * k).x
        r = x1 % n
        if r == 0:
            continue
        s = (gmpy2.invert(k, n) * (h + r * d)) % n
        if s == 0:
            continue
        return (r, s) if not leak_k else (r, s, k)


def hack_sign(n, h, r, s, k):
    return (s * k - h) * pow(r, -1, n) % n


def verify(n, p, a, b, x, y, qx, qy, h, r, s):
    if not 0 < r < n or not 0 < s < n:
        return False
    w = int(gmpy2.invert(s, n))
    u1, u2 = (h * w) % n, (r * w) % n

    curve = WeierstrassCurve(p, a, b)
    g, q = WeierstrassPoint(curve, x, y), WeierstrassPoint(curve, qx, qy)

    x2, y2 = u1 * g + u2 * q
    if x2 == 0 and y2 == 0:
        return False
    return x2 % n == r


if __name__ == '__main__':
    import hashlib
    _h = int(hashlib.sha512(b'Some message to sign with love').hexdigest(), 16)

    # non-ec
    _n = 6277101735386680763835789423207666416102355444464034513029
    _p = 10166180298296945823124292919210075131727604842553305172844237120426504009660181174228315517750538489078034338780817839046493778272552164349676717470
    _x = 18446744073833008487
    _d = random.randrange(1, _n)
    _q = (_x * _d) % _p
    # _d = (_q * gmpy2.invert(_x, _p)) % _p
    _r, _s = sign_non_ec(_n, _p, _x, _d, _h)
    assert verify_non_ec(_n, _p, _x, _q, _h, _r, _s)
    assert not verify_non_ec(_n, _p, _x, _q, _h, _r + 1, _s)
    assert not verify_non_ec(_n, _p, _x, _q, _h, _r, _s + 1)

    # ec
    _n = 91117516390715767613898384092544420415028236560683
    _a = 15220988388919254814683438183226715699820152317943893666355226384525110610174208653373578925471368475180875
    _b = 15041187281250144937602908128761138944594805640214218298857262775127711350895273375824132909615031345071147
    _p = 9173994463960286046443283581208347763186259956673124494950355357547691504353939232280074212440502746218551
    _x = 2003211441495280373681580353135989451096454735271877946445796761562828872438369708705211942304609816501492
    _y = 7951182218206898899336236765984839060728162606719381140630843891613237674570309194342424205313396423149359
    _curve = WeierstrassCurve(_p, _a, _b)
    _g = WeierstrassPoint(_curve, _x, _y)
    _d = random.randrange(1, _n)
    _q = _g * _d
    _qx, _qy = _q.x, _q.y
    _r, _s = sign(_n, _p, _a, _b, _x, _y, _d, _h)
    assert verify(_n, _p, _a, _b, _x, _y, _qx, _qy, _h, _r, _s)
    assert not verify(_n, _p, _a, _b, _x, _y, _qx, _qy, _h, _r + 1, _s)
    assert not verify(_n, _p, _a, _b, _x, _y, _qx, _qy, _h, _r, _s + 1)

    _r, _s, _k = sign(_n, _p, _a, _b, _x, _y, _d, _h, True)
    assert _d == hack_sign(_n, _h, _r, _s, _k)
