import json
from random import randint, choice

signs = ["+", "-", "*", "/"]


def generator(rand_min, rand_max, brackets, min, max):
    count = randint(rand_min, rand_max)

    def combine(nums, operators):
        result = ""
        op = 0
        for num in nums:
            if op < len(operators):
                if operators[op] == "(":
                    result += operators[op]
                    result += num[1:-1] if num.find("-") == 1 else num
                    result += operators[op + 1]
                    op += 2
                    continue
                elif operators[op] == ")":
                    result += num + operators[op]
                    if (op + 1) < len(operators):
                        op += 1
                        result += operators[op]
                        op += 1
                    continue
            result += num
            if op < len(operators):
                result += operators[op]
                op += 1
        return result

    nums = [randint(min, max) for _ in range(count)]
    operators = [choice(signs) for _ in range(count - 1)]

    for i in range(len(nums)):
        if nums[i] < 0 and i != 0:
            nums[i] = f"({nums[i]})"
        else:
            nums[i] = str(nums[i])

    orig_operators = operators.copy()
    wo_bracets = combine(nums, orig_operators)

    if brackets and count > 2:
        open_bracket = randint(0, len(operators) - 2)
        close_bracket = randint(
            open_bracket + 2,
            len(operators) if open_bracket == 0 else len(operators) + 1,
        )
        operators.insert(open_bracket, "(")
        operators.insert(close_bracket, ")")
        with_bracets = combine(nums, operators)

        try:
            if eval(with_bracets) == eval(wo_bracets):
                return wo_bracets
            else:
                return with_bracets
        except ZeroDivisionError:
            return "0/0"
    return wo_bracets


if __name__ == "__main__":
    pass
