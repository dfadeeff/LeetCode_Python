from dns.name import empty


def simplifyPath(path: str) -> str:
    stack = []
    # chars = [i for i in path]
    chars = path.split("/")

    for char in chars:
        if char == "..":
            if len(stack) > 0:
                stack.pop()
        elif char == "." or char == '':
            continue
        else:
            stack.append(char)

    final = ["/" + i for i in stack]

    # print(chars)
    # print(final)
    s = "".join(final)
    if len(s) == 0:
        s = "/"
    return s


if __name__ == '__main__':
    path1 = "/home/"
    print(simplifyPath(path1))
    path2 = "/home//foo/"
    print(simplifyPath(path2))
    path3 = "/a/b///c/.././d/../f/"
    print(simplifyPath(path3))
    path4 = "/home/user/Documents/../Pictures"
    print(simplifyPath(path4))
    path5 = "/../"
    print(simplifyPath(path5))
