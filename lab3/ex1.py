def main():
    f = open("dane.txt", "r")
    data = set(f.read().splitlines())
    print(expr(reduce(data)))


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
                result += '!'
            result += "ABCDEFGHIJKLMNOPRSTUWYZ"[i] + '&'
        result2 += '(' + result[:-1] + ')|'
    return result2[:-1]


main()
