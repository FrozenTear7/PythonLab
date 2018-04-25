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


def latch(s1, s2):
    result = ""
    counter = 0
    for i in range(len(s1)):
        if s1[i] == s2[i]:
            result += s1[i]
        else:
            result += '-'
            counter += 1

    if counter == 1:
        return result
    else:
        return False


def reduce(data):
    result = set()
    f2 = False
    for x in data:
        f1 = False
        for y in data:
            tmp = latch(x, y)
            if tmp:
                result.add(tmp)
                f1 = True
                f2 = True
        if not f1:
            result.add(x)
    if f2:
        return reduce(result)
    return result


def expr(data):
    result2 = ""
    for x in data:
        result = ""
        for i in range(len(x)):
            if x[i] == '-':
                continue
            if x[i] == '0':
                result += '~'
            result += "ABCDEFGHIJKLMNOPRSTUWYZ"[i] + '&'
        result2 += '(' + result[:-1] + ')|'
    return result2[:-1]


def main():
    f = open("dane.txt", "r")
    data = set(f.read().splitlines())
    for line in data:
        if not check(line):
            print("ERROR")
            continue
        onp_line = onp(line)
        var_line = var(onp_line)
        data = set()
        for i in gen(len(var_line)):
            if evaluate(onp_line, i):
                data.add(i)
        data = reduce(data)
        print(line + ": " + expr(data))


main()
