from typing import List


class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        results = []

        def backtrack(openCount, closeCount, path):
            # If the path contains 2*n characters, it's a complete combination
            if len(path) == 2 * n:
                results.append("".join(path))
                return

            # If we can still add an opening parenthesis, do so
            if openCount < n:
                path.append('(')
                backtrack(openCount + 1, closeCount, path)
                path.pop()

            # If we can add a closing parenthesis (we have more open than close used)
            if closeCount < openCount:
                path.append(')')
                backtrack(openCount, closeCount + 1, path)
                path.pop()

        backtrack(0, 0, [])
        return results



def main():
    n = 3
    print(Solution().generateParenthesis(n))
    n = 1
    print(Solution().generateParenthesis(n))


if __name__ == '__main__':
    main()