import gmpy2
import math


def generator(p):
    fact = []
    phi = p - 1
    n = phi

    i = 2
    while i * i <= n:
        if n % i == 0:
            fact.append(i)
            while n % i == 0:
                n //= i
        i += 1

    if n > 1:
        fact.append(n)

    for res in range(2, p + 1): 
        ok = True
        i = 0
        while i < len(fact) and ok:
            if gmpy2.powmod(res, phi // fact[i], p) == 1:
                ok = False
            i += 1
        if ok:
            return res

    return -1


def root(a, k, n):
    g = generator(n)
    sq = int(math.sqrt(n)) + 1
    dec = []

    for i in range(1, sq + 1):
        dec.append([gmpy2.powmod(g, (i * sq * k) % (n - 1), n), i])
    dec.sort(key=lambda ai: ai[0])

    any_ans = -1
    for i in range(0, sq):
        my = (gmpy2.powmod(g, (i * k) % (n - 1), n) * a) % n
        for it in dec:
            if it[0] == my:
                any_ans = it[1] * sq - i
                break
        if any_ans != -1:
            break

    if any_ans == -1:
        return 0

    delta = (n - 1) // gmpy2.gcd(k, n - 1)
    ans = []
    cur = any_ans % delta
    while cur < n - 1:
        ans.append(int(gmpy2.powmod(g, cur, n)))
        cur += delta

    ans.sort()

    return ans


if __name__ == "__main__":
    print(gmpy2.powmod(2, 10, 11))  # 1
    print(generator(11))

    print(root(9, 2, 11))  # 3, 8
