# https://github.com/ashutosh1206/Crypton/tree/master/Discrete-Logarithm-Problem/Elliptic-Curve-DLP
# https://gist.github.com/pqlx/d0bdf2d0c4a2aa400b2b52d9bd9b7b65
# https://doc.sagemath.org/html/en/reference/arithmetic_curves/sage/schemes/elliptic_curves/ell_point.html#sage.schemes.elliptic_curves.ell_point.EllipticCurvePoint_finite_field.discrete_log

def check_pohlig_hellman(curve, generator=None):
    order = generator.order() if generator else curve.order()
    factorization = factor(order)

    bsgs_complexity = order.nth_root(2, True)[0] + 1

    logn = log(order, 2)
    pohlig_hellman_complexity = sum(y * (logn + x.nth_root(2, True)[0]) for x, y in factorization)

    return pohlig_hellman_complexity, bsgs_complexity


def check(curve, generator=None):
    ph = check_pohlig_hellman(curve, generator)
    if ph[0] < ph[1]:
        quotient = round(float(ph[1] / ph[0]), 2) - 1
        logs = [round(float(log(x, 2)), 2) for x in ph]
        print(f"Pohlig-Hellman can make ECDLP solving {quotient} times faster")
        print(f"O(2^{logs[1]}) -> O(2^{logs[0]})")


# O(order)
def bruteforce(P, Q):
    T = P
    for d in range(1, P.order() + 1):
        if T == Q:
            return d
        T += P
        d += 1


# O(sqrt(order))
def bsgs(P, Q):
    m = ceil(sqrt(P.order()))

    # baby step
    lookup = {}
    Pi = P.curve()(0)
    for i in range(m):
        lookup[Pi] = i
        Pi += P

    # giant step
    Qi = Q
    T = P * m
    for j in range(m):
        if Qi in lookup:
            return j * m + lookup[Qi]
        Qi -= T
    return None


# use discrete_log() instead
def pohlig_hellman(P, Q):
    n = P.order()
    xs, ps = [], []
    for p, e in factor(n):
        pe = p ^ e
        npe = n // pe
        Pi, Qi = P * npe, Q * npe
        xi = bsgs(Pi, Qi)
        xs.append(xi)
        ps.append(pe)
    return crt(xs, ps)


if __name__ == '__main__':
    _p = random_prime(2^32)
    _curve = EllipticCurve(GF(_p), (2, 3))
    check(_curve)
    _P = _curve.gens()[0]
    _d = randint(1, _P.order() - 1)
    _Q = _P * _d

    # assert _d == bruteforce(_P, _Q)  # too slow
    assert _d == bsgs(_P, _Q)
    assert _d == pohlig_hellman(_P, _Q)
    assert _d == _P.discrete_log(_Q)
