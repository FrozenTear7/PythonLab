import math


def main():
    a = float(input("a-"))
    b = float(input("b-"))
    c = float(input("c-"))

    d = b * b - 4 * a * c

    if d >= 0:
        p = math.sqrt(d)
        x1 = (-b - p) / (2 * a)
        x2 = (-b + p) / (2 * a)
        print("x1: ", x1)
        print("x2: ", x2)


def sp(n):
    summ = 0
    p = 1
    while p < n:
        if n % p == 0:
            summ += p
        p = p + 1
    return summ


print(sp(15))
for (i) in range(10000):
    if sp(sp(i)) == i:
        print(i, sp(i))
# main()
