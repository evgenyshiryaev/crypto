# p, q ~ sqrt(n)
# ed = 1 + kf
# e ~ f  ->  k ~ d
# ed - kn = 1 + k(1 - p - q) = O(d * sqrt(n))


def get_small_d(n, e):
    n_sqrt = int(sqrt(n))
    M = Matrix([[e, n_sqrt], [n, 0]])
    for row in M.LLL():
        d = abs(row[1]) // n_sqrt
        m = randrange(2, n)
        if pow(pow(m, e, n), d, n) == m:
            return d
    return None


_n = 42004724302405294297751453898364502197
_e = 17924546723775007116522646995236610637
print(get_small_d(_n, _e))
