import random


# value with all bits set
def ones(bits=32):
    return (1 << bits) - 1


INT_BYTES = 4
INT_MAX = ones(INT_BYTES * 8)  # 0xffffffff


LONG_BYTES = 8
LONG_MAX = ones(LONG_BYTES * 8)  # 0xffffffffffffffff


# not
def notb(value, bits=32):
    return ones(bits) - value


# rotate left
def rol(value, n, bits=32):
    return (value << n) & ones(bits) | (value >> (bits - n))


# rotate right
def ror(value, n, bits=32):
    return (value << (bits - n)) & ones(bits) | (value >> n)


def bswap(value: int):
    value = value.to_bytes(4, 'little')
    return int.from_bytes(value, 'big')


def unshift_right_xor(value, shift):
    r = 0
    for i in range(32 // shift + 1):
        r ^= value >> (shift * i)
    return r


def unshift_left_mask_xor(value, shift, mask):
    r = 0
    for i in range(0, 32 // shift + 1):
        part_mask = (INT_MAX >> (32 - shift)) << (shift * i)
        part = value & part_mask
        value ^= (part << shift) & mask
        r |= part
    return r


if __name__ == '__main__':
    assert ones(1) == 1
    assert ones(8) == 0xFF

    assert notb(1, 1) == 0
    assert notb(int('01110011', 2), 8) == int('10001100', 2)

    assert rol(0xCAFEBABE, 10) == 0xFAEAFB2B
    assert ror(0xCAFEBABE, 10) == 0xAFB2BFAE

    assert bswap(0x13121110) == 0x10111213

    _value = random.randint(1, INT_MAX)
    _shift = random.randint(0, 32)
    _mask = random.randint(1, INT_MAX)
    # print(_value, _shift, _mask)

    _shift_right_xor = _value ^ (_value >> _shift)
    # print(_shift_right_xor)
    assert _value == unshift_right_xor(_shift_right_xor, _shift)

    _shift_left_mask_xor = _value ^ ((_value << _shift) & _mask)
    # print(_shift_left_mask_xor)
    assert _value == unshift_left_mask_xor(_shift_left_mask_xor, _shift, _mask)
