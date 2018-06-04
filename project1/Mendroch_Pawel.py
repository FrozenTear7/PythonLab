import sys

OP = "&|>/^~"
alphabet = "abcdefghijklmnopqrstuwyz"


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


# get all variables

def get_var(ex):
    result = ""
    for var in ex:
        if var in alphabet:
            result += var
    return "".join(sorted(set(result)))


# expression check

def check(ex):
    state = True
    paren_count = 0
    for z in ex:
        if z == '~':
            continue
        # endif
        if state:
            if z.isalnum():
                state = False
            elif z in ')' + OP:
                return False
            # endif
        else:
            if z in OP:
                state = True
            elif z in '(' or z.isalnum():
                return False
            # endif
        # endif
        if z == '(':
            paren_count += 1
        elif z == ')':
            paren_count -= 1
        # endif
        if paren_count < 0:
            state = False
        # endif
    # endfor
    if paren_count != 0:
        return False
    # endif
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
        # endif
    # endfor
    return -1


# rpn with operators priorities

def rpn(ex):
    if ex == "":
        return ex
    while ex[0] == '(' and ex[-1] == ')' and check(ex[1: -1]):
        ex = ex[1: -1]
    # endwhile
    p = bal(ex, ">")
    if p >= 0:
        return rpn(ex[:p]) + rpn(ex[p + 1:]) + ex[p]
    # endif
    p = bal(ex, "&|/")
    if p >= 0:
        return rpn(ex[:p]) + rpn(ex[p + 1:]) + ex[p]
    # endif
    p = bal(ex, "^")
    if p >= 0:
        return rpn(ex[:p]) + rpn(ex[p + 1:]) + ex[p]
    # endif
    p = bal(ex, "~")
    if p >= 0:
        return rpn(ex[:p]) + rpn(ex[p + 1:]) + ex[p]
    # endif
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
            # endif
        # endif
    # endfor

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
            st.append(IMPL(st.pop(), st.pop()))
        elif z in "/":
            st.append(NAND(st.pop(), st.pop()))
        elif z in "^":
            st.append(XOR(st.pop(), st.pop()))
        # endif
    # endfor

    return st.pop()


# generate binary strings

def gen(n):
    for i in range(2 ** n):
        yield bin(i)[2:].rjust(n, "0")
    # endfor


def latch(s1, s2):
    result = ""
    counter = 0
    for i in range(len(s1)):
        if s1[i] == s2[i]:
            result += s1[i]
        else:
            result += '-'
            counter += 1
        # endif
    # endfor

    if counter == 1:
        return result
    else:
        return False
    # endif


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
            # endif
        # endfor
        if not f1:
            result.add(x)
        # endif
    if f2:
        return reduce(result)
    # endif
    return result


# returns an expression from the reduced form
# also erases unnecessary parentheses

def ex_from_reduced(data, n):
    if len(data) == 0:
        return "F"
    # endif

    # fully reduced to true

    if "".rjust(n, "-") in data:
        return "T"
    # endif

    result2 = ""
    counter = 0
    for x in data:
        counter += 1
        tmp_counter = 0
        result = ""
        for i in range(len(x)):
            if x[i] == '-':
                continue
            # endif
            if x[i] == '0':
                result += '~'
            # endif
            result += alphabet[i] + '&'
            tmp_counter += 1
        if tmp_counter > 1:
            result2 += '(' + result[:-1] + ')|'
        else:
            result2 += result[:-1] + "|"
        # endif
    # endfor
    if counter == 1 and tmp_counter > 1:
        return result2[1:-2]
    else:
        return result2[:-1]
    # endif


def main():
    line = sys.stdin.readline()
    copy_line = line

    line = line.replace(" ", "")
    line = line.replace("~~", "")
    line = line[:-1]

    # if the expression is not correct return ERROR

    if not check(line):
        print("ERROR")
        return

    rpn_line = rpn(line)
    var_line = get_var(rpn_line)
    data = set()

    for i in gen(len(var_line)):
        if evaluate(rpn_line, i):
            data.add(i)
        # endif
    # endfor

    data = reduce(data)
    reduced = ex_from_reduced(data, len(var_line))
    if len(copy_line) < len(reduced):
        print(copy_line)
    else:
        print(reduced)


main()
