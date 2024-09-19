from inspect import stack


def isValid(s: str) -> bool:
    stack = []
    matching = {"(": ")", "[": "]", "{": "}"}

    for c in s:
        if c in matching:
            stack.append(c)
        else:
            if not stack:
                """if the stack with a coming closing bracket is empty, nothing to balance -> return false"""
                return False
            previous_opening = stack.pop()
            if matching[previous_opening] != c:
                return False
    """returns boolean and checks whether stack is empty or not after processing all brackets"""
    return not stack


if __name__ == '__main__':
    s1 = "()"
    print(isValid(s1))
    s2 = "()[]{}"
    print(isValid(s2))
    s3 = "(]"
    print(isValid(s3))
