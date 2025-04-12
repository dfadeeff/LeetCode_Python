from pythonProject.LinkedLists.CopyListRandomPointer import print_list


class Solution:
    def simplifyPath(self, path: str) -> str:
        stack = []
        path_items = path.split('/')
        print(path_items)

        for item in path_items:
            if item == '.' or not item:
                continue
            elif item == '..':
                if stack:
                    stack.pop()
            else:
                stack.append(item)

        return "/" + "/".join(stack)


if __name__ == '__main__':
    path = "/home/user/Documents/../Pictures"
    print(Solution().simplifyPath(path))
