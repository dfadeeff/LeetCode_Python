from collections import defaultdict
from typing import List


class Solution:
    def alienOrder(self, words: List[str]) -> str:
        # Step 1: Build graph
        graph = defaultdict(list)
        letters = set("".join(words))

        for first, second in zip(words, words[1:]):
            for c1, c2 in zip(first, second):
                if c1 != c2:
                    graph[c1].append(c2)
                    break
            else:
                # Check prefix case, invalid order
                if len(second) < len(first):
                    return ""
            # Step 2: DFS with state
        state = {c: 0 for c in letters}
        print(state)
        result = []

        def dfs(node):
            if state[node] == 1:
                return False  # cycle
            if state[node] == 2:
                return True
            state[node] = 1
            for neighbor in graph[node]:
                if not dfs(neighbor):
                    return False
            state[node] = 2
            result.append(node)
            return True

        for c in letters:
            if state[c] == 0:
                if not dfs(c):
                    return ""

        return "".join(result[::-1])  # reverse post-order


if __name__ == '__main__':
    words = ["wrt", "wrf", "er", "ett", "rftt"]
    print(Solution().alienOrder(words))
