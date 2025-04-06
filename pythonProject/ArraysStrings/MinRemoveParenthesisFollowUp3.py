from collections import deque


class Solution:
    def minRemoveToMakeValidStack(self, s: str) -> str:
        # First pass: remove excess ')'
        result = []
        balance = 0
        for c in s:
            if c == '(':
                balance += 1
                result.append(c)
            elif c == ')':
                if balance > 0:
                    balance -= 1
                    result.append(c)
            else:
                result.append(c)

        # Second pass: remove excess '(' from end
        final = []
        balance = 0
        for c in reversed(result):
            if c == '(' and balance > 0:
                balance -= 1
                continue
            if c == ')':
                balance += 1
            final.append(c)

        return ''.join(reversed(final))


if __name__ == '__main__':
    s = "lee(t(c)o)de)"  # last unmatched parenthesis at index 12
    print(Solution().minRemoveToMakeValidStack(s))
