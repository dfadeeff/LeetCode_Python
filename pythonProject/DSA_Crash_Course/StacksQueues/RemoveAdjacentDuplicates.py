from inspect import stack


def removeDuplicates(s: str) -> str:

    stack = []
    for c in s:

        # equivalent to stack != [] and stack[-1] == c:
        # empty list [] treated as false and non-empty as True
        if stack and stack[-1] == c:
            stack.pop()
        else:
            stack.append(c)
    return ''.join(stack)

if __name__ == '__main__':
    s1 = "abbaca"
    print(removeDuplicates(s1))
    s2 = "azxxzy"
    print(removeDuplicates(s2))
