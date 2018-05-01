import sys

OP = "&|>/^~"
alphabet = "abcdefghijklmnoprstuwyz"


# defined operations

def OR(a, b):
    return a or b


def AND(a, b):
    return a and b


def NAND(a, b):
    return 1 - (a and b)


def IMPL(a, b):
    return a or (1 - b)


def XOR(a, b):
    return OR(AND(a, (1 - b)), AND((1 - a), b))


def get_var(ex):
    w = [z for z in ex if z.isalnum()]
    return "".join(sorted(set(w)))


# expression check

def check(ex):
    state = True
    paren_count = 0
    for z in ex:
        if z == '~':
            continue
        if state:
            if z.isalnum():
                state = False
            elif z in ')' + OP:
                return False
        else:
            if z in OP:
                state = True
            elif z in '(' or z.isalnum():
                return False
        if z == '(':
            paren_count += 1
        elif z == ')':
            paren_count -= 1
        if paren_count < 0:
            state = False
    if paren_count != 0:
        return False
    return not state


# find operation index

def bal(ex, op):
    paren_count = 0
    for i in range(len(ex) - 1, -1, -1):
        if ex[i] == '(':
            paren_count += 1
        elif ex[i] == ')':
            paren_count -= 1
        elif ex[i] in op and paren_count == 0:
            return i
    return -1


# rpn with operators priorities

def rpn(ex):
    if ex == "":
        return ex
    while ex[0] == '(' and ex[-1] == ')' and check(ex[1: -1]):
        ex = ex[1: -1]
    p = bal(ex, ">")
    if p >= 0:
        return rpn(ex[:p]) + rpn(ex[p + 1:]) + ex[p]
    p = bal(ex, "&|/")
    if p >= 0:
        return rpn(ex[:p]) + rpn(ex[p + 1:]) + ex[p]
    p = bal(ex, "^")
    if p >= 0:
        return rpn(ex[:p]) + rpn(ex[p + 1:]) + ex[p]
    p = bal(ex, "~")
    if p >= 0:
        return rpn(ex[:p]) + rpn(ex[p + 1:]) + ex[p]
    return ex


def map(ex, var, val):
    l = list(ex)
    for i in range(len(l)):
        if l[i] in "F":
            l[i] = "0"
        elif l[i] in "T":
            l[i] = "1"
        else:
            p = var.find(l[i])
            if p >= 0:
                l[i] = val[p]

    return "".join(l)


def evaluate(ex, val):
    zm = get_var(ex)
    ex = map(ex, zm, val)
    st = []
    for z in ex:
        if z in "01":
            st.append(int(z))
        elif z in "~":
            st.append(1 - st.pop())
        elif z in "|":
            st.append(OR(st.pop(), st.pop()))
        elif z in "&":
            st.append(AND(st.pop(), st.pop()))
        elif z in ">":
            st.append(IMPL(st.pop(), (1 - st.pop())))
        elif z in "/":
            st.append(NAND(st.pop(), st.pop()))
        elif z in "^":
            st.append(XOR(st.pop(), st.pop()))
    return st.pop()


# generate binary strings

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


# Quine McCluskey algorithm for logic reduction

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


def check_true(data):
    for x in data:
        if x != '-':
            return True
    return False


# returns an expression from the reduced form
# also erases unnecessary parentheses

def ex_from_reduced(data):
    if len(data) == 0:
        return "F"

    # fully reduced to true

    # if check_true(data):
    #     return "T"

    result2 = ""
    counter = 0
    for x in data:
        counter += 1
        tmp_counter = 0
        result = ""
        for i in range(len(x)):
            if x[i] == '-':
                continue
            if x[i] == '0':
                result += '~'
            result += alphabet[i] + '&'
            tmp_counter += 1
        if tmp_counter > 1:
            result2 += '(' + result[:-1] + ')|'
        else:
            result2 += result[:-1] + "|"
    if counter == 1 and tmp_counter > 1:
        return result2[1:-2]
    else:
        return result2[:-1]


def main():
    while 1:
        try:
            line = sys.stdin.readline()

            # erase unwanted spaces and double negations

            line = line.replace(" ", "")
            line = line.replace("~~", "")

            # if the expression is not correct return ERROR

            if not check(line):
                print("ERROR")
                continue
            rpn_line = rpn(line)
            var_line = get_var(rpn_line)
            data = set()
            for i in gen(len(var_line)):
                if evaluate(rpn_line, i):
                    data.add(i)
            data = reduce(data)
            print(line + ": " + ex_from_reduced(data))

        except KeyboardInterrupt:
            break

        if not line:
            break


main()
