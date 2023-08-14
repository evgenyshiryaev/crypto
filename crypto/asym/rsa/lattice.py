# p, q ~ sqrt(n)
# ed = 1 + kf
# e ~ f  ->  k ~ d
# ed - kn = 1 + k(1 - p - q) = O(d * sqrt(n))


import gmpy2
import numpy as np
import random
from utils.lattice import gaussian_lr


def get_small_d(n, e):
    gmpy2.get_context().precision = n.bit_length()
    n_sqrt = int(gmpy2.sqrt(n))
    for row in gaussian_lr(np.array([e, n_sqrt], dtype=object), np.array([n, 0], dtype=object)):
        d = abs(row[1]) // n_sqrt
        m = random.randrange(2, n)
        if pow(pow(m, e, n), d, n) == m:
            return d
    return None


_n = 42004724302405294297751453898364502197
_e = 17924546723775007116522646995236610637
assert get_small_d(_n, _e) == 814510573
