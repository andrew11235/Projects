import itertools


def get_ops_perms(disallowed=None) -> list:
    if disallowed is None:
        disallowed = []

    allowed = ["+", "-", "/", "*"]

    for o in disallowed:
        allowed.remove(o)

    ops = []
    for o in allowed:
        ops += (3 * [o])

    perms = list(itertools.permutations(ops, 3))

    perms_str = []

    for p in perms:
        perms_str.append("".join(p))

    return list(set(perms_str))


def get_nums_perms(nums: str) -> list:
    perms = list(itertools.permutations(nums))

    perms_str = []

    for p in perms:
        perms_str.append("".join(p))

    return list(set(perms_str))


def get_expressions(nums: list, ops: list) -> list:
    paras = [[0, 4], [0, 6], [2, 6], [2, 8], [4, 8]]

    exps = []
    for n in nums:
        for o in ops:
            expression = [n[0], o[0], n[1], o[1], n[2], o[2], n[3]]

            exps.append("".join(expression))

            for p in paras:
                expression_p = expression.copy()
                expression_p.insert(p[0], "(")
                expression_p.insert(p[1], ")")

                exps.append("".join(expression_p))

    return exps


def get_solutions(exps: list, target: int = 10.0) -> list:
    solutions = []

    for e in exps:
        try:
            res = round(eval(e), 1)
        except ZeroDivisionError:
            continue

        # print(e + " = " + str(res))

        if res == target:
            solutions.append(e)

    return solutions


def main():
    ops = get_ops_perms(disallowed=[])

    nums = get_nums_perms("1234")

    exps = get_expressions(nums, ops)

    solutions = get_solutions(exps)

    if len(solutions) == 0:
        print("no solutions")

    else:
        for s in solutions:
            print(s)


if __name__ == '__main__':
    main()
