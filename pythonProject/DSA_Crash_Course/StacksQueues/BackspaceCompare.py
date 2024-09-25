from inspect import stack


def backspaceCompare(s: str, t: str) -> bool:
    def build(s):
        stack = []
        for c in s:
            if c != "#":
                stack.append(c)
            elif stack:
                stack.pop()

        return "".join(stack)

    return build(s) == build(t)


if __name__ == '__main__':
    s1 = "ab#c"
    t1 = "ad#c"
    print(backspaceCompare(s1, t1))
    s2 = "ab##"
    t2 = "c#d#"
    print(backspaceCompare(s2, t2))
