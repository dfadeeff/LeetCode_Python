class Solution:
    def simplifyPath(self, cwd: str, cd: str) -> str:
        stack = []

        def process_path(path):
            for item in path.split('/'):
                if item == '' or item == '.':
                    continue
                elif item == '..':
                    if stack:
                        stack.pop()
                else:
                    stack.append(item)

        # First process current working directory
        process_path(cwd)

        # Then apply cd command
        process_path(cd)

        return '/' + '/'.join(stack)


if __name__ == '__main__':
    cwd = "/a/b/c"
    cd = "/d/./e"
    print(Solution().simplifyPath(cwd, cd))  # Output: "/d/e"

    cwd = ""
    cd = "/d/./e"
    print(Solution().simplifyPath(cwd, cd))  # Output: "/d/e"
