from typing import List


class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        stack = []
        for token in tokens:
            if token not in {"-","+","*","/"}:
                stack.append(int(token))
            else:
                b = stack.pop()
                a = stack.pop()
                if token == "+":
                    stack.append(a+b)
                elif token == "-":
                    stack.append(a-b)
                elif token == "*":
                    stack.append(a*b)
                elif token == "/":
                    stack.append(int(a/b))


        return stack[0]


if __name__ == '__main__':
    tokens = ["2", "1", "+", "3", "*"]
    print(Solution().evalRPN(tokens))
    tokens = ["4", "13", "5", "/", "+"]
    print(Solution().evalRPN(tokens))

