from typing import List

from collections import defaultdict


class Solution:
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        graph = defaultdict(list)

        for from_edge, to_edge in edges:
            graph[from_edge].append(to_edge)
            graph[to_edge].append(from_edge)

        seen = set()
        provinces = 0

        def dfs(node):
            seen.add(node)
            for neighbor in graph[node]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    dfs(neighbor)

        for i in range(n):
            if i not in seen:
                provinces += 1
                seen.add(i)
                dfs(i)

        return provinces


if __name__ == "__main__":
    sol = Solution()
    n = 5
    edges = [[0, 1], [1, 2], [3, 4]]
    print(sol.countComponents(n, edges))
