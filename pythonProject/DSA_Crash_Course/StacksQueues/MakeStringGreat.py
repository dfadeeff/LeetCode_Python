def makeGood(s: str) -> str:
    stack = []

    for c in s:
        if stack and c.isupper() and stack[-1] == c.lower() :
            stack.pop()
        elif stack and c.islower() and stack[-1] == c.upper() :
            stack.pop()
        else:
            stack.append(c)
    return ''.join(stack)


if __name__ == '__main__':
    s1 = "leEeetcode"
    print(makeGood(s1))
    s2 = "abBAcC"
    print(makeGood(s2))
