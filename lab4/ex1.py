def podz(n):
    for i in range(1, n):
        if n % i == 0:
            yield i


def primes():
    l = [2]
    p = 2
    yield p
    while True:
        p += 1
        for q in l:
            if p % q == 0:
                break
        else:
            l.append(p)
            yield p


def rozklad(n):
    for p in primes():
        while n % p == 0:
            n = n / p
            yield p
        if n == 1:
            break


def gen(n):
    if n == 0:
        yield ""
    else:
        for c in gen(n - 1):
            yield c + '0'
            yield c + '1'


def perm(n):
    if len(n) == 1:
        yield n
    else:
        for p in perm(n[1:]):
            for i in range(len(n)):
                yield p[:i] + n[0] + p[i:]


def kombinacja(s, k):
    if len(s) == k:
        yield s
    elif k == 0:
        yield ""
    else:
        for k1 in kombinacja(s[1:], k):
            yield k1
        for k1 in kombinacja(s[1:], k - 1):
            yield s[0] + k1


def wariacja(s, k):
    for ko in kombinacja(s, k):
        for p in perm(ko):
            yield p


for i in wariacja('abcd', 2):
    print(i)
