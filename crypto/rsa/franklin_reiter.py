# http://blog.redrocket.club/2017/11/27/TUCTF-CryptoClock/

import Crypto.Util.number
import sympy


def franklin_reiter(n, e, c0, a0, b0, c1, a1, b1):
    x = sympy.symbols('x')
    g0 = sympy.poly((a0 * x + b0) ** e - c0).set_modulus(n)
    g1 = sympy.poly((a1 * x + b1) ** e - c1).set_modulus(n)
    return -sympy.gcd(g0, g1).coeffs()[-1]


if __name__ == '__main__':
    _p, _q = Crypto.Util.number.getPrime(256), Crypto.Util.number.getPrime(256)
    _n = _p * _q
    _e = 3

    _m = b'This is super secret message noone can read'
    _pad0 = Crypto.Util.number.bytes_to_long(b'some padding')
    _pad1 = Crypto.Util.number.bytes_to_long(b'just another one')
    _c0 = pow(Crypto.Util.number.bytes_to_long(_m) + _pad0, _e, _n)
    _c1 = pow(Crypto.Util.number.bytes_to_long(_m) + _pad1, _e, _n)

    _m_hacked = franklin_reiter(_n, _e, _c0, 1, _pad0, _c1, 1, _pad1)
    assert _m == Crypto.Util.number.long_to_bytes(_m_hacked)
