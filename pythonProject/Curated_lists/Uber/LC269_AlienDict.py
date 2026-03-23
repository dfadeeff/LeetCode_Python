from typing import List
from collections import defaultdict, deque

class Solution:
    def alienOrder(self, words: List[str]) -> str:
        """
        Only adjacent words give us ordering info

        "wrt" vs "wrf" → first difference at index 2
                  t vs f → t comes before f
                  edge: t → f

        "wrf" vs "er"  → first difference at index 0
                  w vs e → w comes before e
                  edge: w → e

        "er"  vs "ett" → first difference at index 1
                  r vs t → r comes before t
                  edge: r → t

        "ett" vs "rftt"→ first difference at index 0
                  e vs r → e comes before r
                  edge: e → r

        edges:
            t → f
            w → e
            r → t
            e → r


        """

        # all unique chars, start with in_degree=0
        graph = defaultdict(set)
        in_degree = {c: 0 for word in words for c in word}

        # compare adjacent words
        for i in range(len(words) - 1):
            w1, w2 = words[i], words[i + 1]
            min_len = min(len(w1), len(w2))

            # invalid: longer word is prefix of shorter
            if len(w1) > len(w2) and w1[:min_len] == w2[:min_len]:
                return ""

            # find first difference → one edge
            for j in range(min_len):
                if w1[j] != w2[j]:
                    if w2[j] not in graph[w1[j]]:
                        graph[w1[j]].add(w2[j])
                        in_degree[w2[j]] += 1
                    break

        # Kahn's BFS — identical to 210

        queue = deque(c for c in in_degree if in_degree[c] == 0)
        order = []

        while queue:
            c = queue.popleft()
            order.append(c)
            for nb in graph[c]:
                in_degree[nb] -= 1
                if in_degree[nb] == 0:
                    queue.append(nb)
        # cycle = some chars never processed

        if len(order) != len(in_degree):
            return ""

        return "".join(order)


if __name__ == "__main__":
    sol = Solution()
    words = ["wrt", "wrf", "er", "ett", "rftt"]
    print(sol.alienOrder(words))
