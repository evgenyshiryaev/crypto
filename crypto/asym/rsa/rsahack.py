# https://github.com/RsaCtfTool/RsaCtfTool
# ./RsaCtfTool.py --createpub -n n -e e > key.pub
# ./RsaCtfTool.py --publickey key.pub --private --dump


import gmpy2


def small_m_large_n(n, e, c):
    gmpy2.get_context().precision = gmpy2.bit_length(c)
    m = int(gmpy2.root(c, e))
    assert pow(m, e, n) == c
    return m


if __name__ == '__main__':
    from Crypto.Util.number import getPrime, getRandomNBitInteger

    _BITS = 256

    _n = getPrime(_BITS) * getPrime(_BITS)
    _m = getRandomNBitInteger(8)
    _e = 3
    _c = pow(_m, _e, _n)
    assert _m == small_m_large_n(_n, _e, _c)
