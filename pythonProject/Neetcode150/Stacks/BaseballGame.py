from typing import List


class Solution:
    def calPoints(self, operations: List[str]) -> int:
        stack = []
        for ch in operations:
            if ch == "+":
                stack.append(stack[-1] + stack[-2])
            elif ch == "C":
                stack.pop()
            elif ch == "D":
                stack.append(2 * stack[-1])
            else:
                stack.append(int(ch))

        total = 0
        for i in stack:
            total += i
        return total


if __name__ == "__main__":
    ops = ["5", "2", "C", "D", "+"]
    print(Solution().calPoints(ops))
