from typing import List


class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        # only add open parenthesis if open < n
        # only add closing parenthesis if closed < open
        # valid IFF open == closed == n

        stack = []
        res = []

        def backtrack(openN, closeN):
            if openN == closeN == n:
                res.append("".join(stack))
                return
            if openN < n:
                stack.append("(")
                backtrack(openN + 1, closeN)
                stack.pop()

            if closeN < openN:
                stack.append(")")
                backtrack(openN, closeN + 1)
                stack.pop()
        backtrack(0,0)
        return res


if __name__ == "__main__":
    n = 3
    print(Solution().generateParenthesis(n))
