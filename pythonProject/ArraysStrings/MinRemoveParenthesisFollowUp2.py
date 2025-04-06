from collections import deque


class Solution:
    def minRemoveToMakeValidStack(self, s: str) -> str:
        """Remove the minimum number of invalid parentheses and return all results"""

        def isValid(string):
            balance = 0
            for c in string:
                if c == '(':
                    balance += 1
                elif c == ')':
                    balance -= 1
                    if balance < 0:
                        return False
            return balance == 0

        queue = deque([s])
        visited = set()
        results = []
        found = False

        while queue:
            current = queue.popleft()
            if isValid(current):
                results.append(current)
                found = True
            if found:
                continue  # only collect shortest valid strings
            for i in range(len(current)):
                if current[i] not in '()':
                    continue
                candidate = current[:i] + current[i + 1:]
                if candidate not in visited:
                    visited.add(candidate)
                    queue.append(candidate)

        return results



if __name__ == '__main__':
    s = "lee(t(c)o)de)"  # last unmatched parenthesis at index 12
    print(Solution().minRemoveToMakeValidStack(s))
