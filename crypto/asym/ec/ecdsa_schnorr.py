# https://en.wikipedia.org/wiki/Schnorr_signature
# https://crypto.stackexchange.com/questions/34863/ec-schnorr-signature-multiple-standard

from crypto.asym.ec.ec_weierstrass import WeierstrassCurve, WeierstrassPoint
from Crypto.Util.number import bytes_to_long
import hashlib
import random


def sign(n, p, a, b, x, y, d, m):
    curve = WeierstrassCurve(p, a, b)
    g = WeierstrassPoint(curve, x, y)
    k = random.randrange(1, _n)
    r = g * k
    e = bytes_to_long(hashlib.sha256(r.to_bytes() + m).digest()) % n
    s = (k - d * e) % n
    return s, e


def verify(n, p, a, b, x, y, qx, qy, m, s, e):
    if not 0 < s < n or not 0 < e < n:
        return False

    curve = WeierstrassCurve(p, a, b)
    g, q = WeierstrassPoint(curve, x, y), WeierstrassPoint(curve, qx, qy)

    rv = g * s + q * e
    ev = bytes_to_long(hashlib.sha256(rv.to_bytes() + m).digest()) % n
    return ev == e


if __name__ == '__main__':
    _m = b'Some message to sign with love'
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
    _s, _e = sign(_n, _p, _a, _b, _x, _y, _d, _m)
    assert verify(_n, _p, _a, _b, _x, _y, _qx, _qy, _m, _s, _e)
    assert not verify(_n, _p, _a, _b, _x, _y, _qx, _qy, _m, _s + 1, _e)
    assert not verify(_n, _p, _a, _b, _x, _y, _qx, _qy, _m, _s, _e + 1)
