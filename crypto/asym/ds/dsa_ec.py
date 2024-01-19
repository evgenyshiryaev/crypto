# https://cryptobook.nakov.com/digital-signatures/ecdsa-sign-verify-messages
# https://en.wikipedia.org/wiki/Elliptic_Curve_Digital_Signature_Algorithm

from crypto.asym.ec.ec_weierstrass import WeierstrassCurve, WeierstrassPoint
import random


# n - order
# p - prime
# a, b - curve params
# (x, y) - base point
# d - private key
# (qx, qy) - public key
# k - nonce
def sign(n, p, a, b, x, y, d, h, k=None, leak_k=False):
    curve = WeierstrassCurve(p, a, b)
    g = WeierstrassPoint(curve, x, y)
    while True:
        if k is None:
            k = random.randrange(1, n)
        x1 = (g * k).x
        r = x1 % n
        if r == 0:
            continue
        s = pow(k, -1, n) * (h + r * d) % n
        if s == 0:
            continue
        return (r, s) if not leak_k else (r, s, k)


def verify(n, p, a, b, x, y, qx, qy, h, r, s):
    if not 0 < r < n or not 0 < s < n:
        return False
    w = pow(s, -1, n)
    u1, u2 = h * w % n, r * w % n

    curve = WeierstrassCurve(p, a, b)
    g, q = WeierstrassPoint(curve, x, y), WeierstrassPoint(curve, qx, qy)

    x2, y2 = u1 * g + u2 * q
    if x2 == 0 and y2 == 0:
        return False
    return x2 % n == r


# s = k^-1 * (h + r * d)
# d = (s * k - h) * r^-1
def hack_known_k(n, h, r, s, k):
    return (s * k - h) * pow(r, -1, n) % n


# k * s0 = h0 + r * d
# k * s1 = h1 + r * d
# r is same for same k
# k = (h1 - h0) * (s1 - s0)^-1
def hack_same_k(n, h0, h1, s0, s1):
    return (h1 - h0) * pow(s1 - s0, -1, n) % n


if __name__ == '__main__':
    import hashlib
    _h = int(hashlib.sha512(b'Some message to sign with love').hexdigest(), 16)

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

    _r, _s, _k = sign(_n, _p, _a, _b, _x, _y, _d, _h, None, True)
    assert _d == hack_known_k(_n, _h, _r, _s, _k)

    _h1 = int(hashlib.sha512(b'Just another message to sign with love').hexdigest(), 16)
    _, _s1 = sign(_n, _p, _a, _b, _x, _y, _d, _h1, _k)
    assert _k == hack_same_k(_n, _h, _h1, _s, _s1)
