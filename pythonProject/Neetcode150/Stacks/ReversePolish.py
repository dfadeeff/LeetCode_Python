from typing import List


class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        stack = []
        for ch in tokens:
            if ch == "+":
                stack.append(stack.pop() + stack.pop())
            elif ch == "-":
                a, b = stack.pop(), stack.pop()
                stack.append(b - a)
            elif ch == "*":
                stack.append(stack.pop() * stack.pop())
            elif ch == "/":
                a, b = stack.pop(), stack.pop()
                stack.append(int(float(b) / a))
            else:
                stack.append(int(ch))
        return stack[0]


if __name__ == "__main__":
    tokens = ["2", "1", "+", "3", "*"]
    print(Solution().evalRPN(tokens))
