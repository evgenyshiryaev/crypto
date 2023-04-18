import random


INT_BYTES = 4
INT_MAX = (1 << (INT_BYTES * 8)) - 1  # 0xffffffff

LONG_BYTES = 8
LONG_MAX = (1 << (LONG_BYTES * 8)) - 1  # 0xffffffffffffffff


def rotate_left(value, n, bits=32):
    return (value << n) | (value >> (bits - n))


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
    _value = random.randint(1, INT_MAX)
    _shift = random.randint(0, 32)
    _mask = random.randint(1, INT_MAX)
    print(_value, _shift, _mask)

    _shift_right_xor = _value ^ (_value >> _shift)
    print(_shift_right_xor)
    assert _value == unshift_right_xor(_shift_right_xor, _shift)

    _shift_left_mask_xor = _value ^ ((_value << _shift) & _mask)
    print(_shift_left_mask_xor)
    assert _value == unshift_left_mask_xor(_shift_left_mask_xor, _shift, _mask)
