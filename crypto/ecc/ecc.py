# https://cryptobook.nakov.com/asymmetric-key-ciphers/elliptic-curve-cryptography-ecc
# y2 = x3 + ax + b (mod p) - Weierstrass
# by2 = x3 + ax2 + x - Montgomery
# x2 + y2 = 1 + dx2y2 - Edwards
# 0 ≤ x, y < p

# n = h * r
# n - order of curve / entire group
# h - cofactor, number of cyclic subgroups / partitions
# r - order of each subgroup, can be different in n is not prime

# G - generator / base point
# all points = G * [0..r)
# 0 * G = r * G - infinity

# k - private key (integer)
# P = k * G - public key (point)


from nummaster.basic import sqrtmod
import secrets
from tinyec import registry
from tinyec.ec import Curve, SubGroup


def print_curve(c):
    print('Curve:', c)
    print(f'n={c.field.n} h={c.field.h} G={c.field.g}')


def compress_point(point):
    # another way - f'0{2 + y % 2}{hex(pubKey.x)[2:]}'
    return point[0], point[1] & 1


def uncompress_point(cpoint, p, a, b):
    x, is_odd = cpoint
    y = sqrtmod(pow(x, 3, p) + a * x + b, p)
    return (x, y) if bool(is_odd) == bool(y & 1) else (x, p - y)


def p1707():
    field = SubGroup(p=17, g=(15, 13), n=18, h=1)
    curve = Curve(a=0, b=7, field=field, name='p1707')
    print_curve(curve)

    for k in range(0, curve.field.n + 1):
        p = k * curve.g
        print(f'{k} * G = ({p.x}, {p.y})')


def secp192r1():
    curve = registry.get_curve('secp192r1')
    print_curve(curve)

    for k in range(0, 5):
        p = k * curve.g
        print(f'{k} * G = ({p.x}, {p.y})')
    print('.....')

    nG = curve.field.n * curve.g
    print(f'n * G = ({nG.x}, {nG.y})')

    private_key = secrets.randbelow(curve.field.n)
    public_key = private_key * curve.g
    print(f'Private key = {private_key}')
    print(f'Public key = {public_key}')

    cpublic_key = compress_point((public_key.x, public_key.y))
    print(cpublic_key)
    print(uncompress_point(cpublic_key, curve.field.p, curve.a, curve.b))


if __name__ == '__main__':
    p1707()
    print()

    secp192r1()
    print()
