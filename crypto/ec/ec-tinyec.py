from crypto.ec.ec import compress_point, uncompress_point
import secrets
from tinyec import registry
from tinyec.ec import Curve, SubGroup


def print_curve(c):
    print('Curve:', c)
    print(f'n={c.field.n} h={c.field.h} G={c.field.g}')


def p1707():
    field = SubGroup(p=17, g=(15, 13), n=18, h=1)
    curve = Curve(a=0, b=7, field=field, name='p1707')
    print_curve(curve)

    for k in range(curve.field.n + 1):
        p = k * curve.g
        print(f'{k} * G = ({p.x}, {p.y})')


def secp192r1():
    curve = registry.get_curve('secp192r1')
    print_curve(curve)

    for k in range(5):
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
