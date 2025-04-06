from collections import deque


class Solution:
    def minRemoveToMakeValidStack(self, s: str) -> str:
        """in place"""
        s = list(s)  # Work with mutable list
        stack = []

        # First pass: mark invalid ')'
        for i, c in enumerate(s):
            if c == '(':
                stack.append(i)
            elif c == ')':
                if stack:
                    stack.pop()
                else:
                    s[i] = ''  # Mark invalid ')'

        # Second pass: mark unmatched '('
        while stack:
            idx = stack.pop()
            s[idx] = ''  # Mark invalid '('

        return ''.join(s)


if __name__ == '__main__':
    s = "lee(t(c)o)de)"  # last unmatched parenthesis at index 12
    print(Solution().minRemoveToMakeValidStack(s))
