# https://en.wikipedia.org/wiki/Euler%27s_totient_function
# see sympy.ntheory.primitive_root()

# f - Euler totient function
# f(1)=1
# f(9)=6 - 1,2,4,5,7,8
# f(pq)=f(p)f(q) if gcd(p,q)=1
# f(n)=p0^k0-1(p0-1) * ... if n=p0^k0 * ...
# a^f(n)=1 mod n - Euler theorem
# a^p-1=1 mod p - Fermat little theorem

# |GF(p)|=f(p)=p-1
# |G|=f(f(p))=f(p-1), if G=<GF(p)> - all generators

from sympy.ntheory import primefactors


def gens_bruteforce(p):
    gens = []
    for gen in range(2, p):
        a = gen
        cnt = 1
        while a != 1:
            a = a * gen % p
            cnt += 1
        if cnt == p - 1:
            gens.append(gen)
    return gens


def gens_euler(p):
    f = p - 1
    factors = set(primefactors(f))
    gens = []
    for gen in range(2, p):
        found = True
        for factor in factors:
            if pow(gen, f // factor, p) == 1:
                found = False
                break
        if found:
            gens.append(gen)
    return gens


if __name__ == '__main__':
    import sympy.ntheory

    assert gens_bruteforce(7) == [3, 5]
    assert gens_euler(7) == [3, 5]
    assert sympy.ntheory.primitive_root(7) == 3
    # sage: primitive_root(7)
