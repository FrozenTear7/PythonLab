OP = "&|>"


def var(wyr):
    w = [z for z in wyr if z.isalnum()]
    return "".join(sorted(set(w)))


def check(wyr):
    state = True
    ln = 0
    for z in wyr:
        if state:
            if z.isalnum():
                state = False
            elif z in ")" + OP:
                return False
        else:
            if z in OP:
                state = True
            elif z in "(" or z.isalnum():
                return False
        if z == '(':
            ln += 1
        elif z == ')':
            ln -= 1
        if ln < 0:
            state = False
    if ln != 0:
        return False
    return not state


def bal(wyr, op):
    ln = 0
    for i in range(len(wyr) - 1, 0, -1):
        if wyr[i] == '(':
            ln += 1
        elif wyr[i] == ')':
            ln -= 1
        elif wyr[i] in op and ln == 0:
            return i
    return -1


def onp(wyr):
    while wyr[0] == '(' and wyr[-1] == ')' and check(wyr[1: -1]):
        wyr = wyr[1: -1]
    p = bal(wyr, ">")
    if p >= 0:
        return onp(wyr[:p]) + onp(wyr[p + 1:]) + wyr[p]
    p = bal(wyr, "&|")
    if p >= 0:
        return onp(wyr[:p]) + onp(wyr[p + 1:]) + wyr[p]
    return wyr


def mapuj(wyr, zm, wart):
    l = list(wyr)
    for i in range(len(l)):
        p = zm.find(l[i])
        if p >= 0:
            l[i] = wart[p]

    return "".join(l)


def OR(a, b):
    return a or b


def AND(a, b):
    return a and b


def evaluate(wyr, val):
    zm = var(wyr)
    wyr = mapuj(wyr, zm, val)
    st = []
    for z in wyr:
        if z in "01":
            st.append(int(z))
        elif z in "|":
            st.append(OR(st.pop(), st.pop()))
        elif z in "&":
            st.append(AND(st.pop(), st.pop()))
        elif z in ">":
            st.append(st.pop() or (1 - st.pop()))
    return st.pop()


def gen(n):
    for i in range(2 ** n):
        yield bin(i)[2:].rjust(n, "0")


while True:
    wyr = input(">>")
    wyr = onp(wyr)
    zm = var(wyr)
    for val in gen(len(zm)):
        print(val, evaluate(wyr, val))
