from collections import defaultdict
from typing import List


class Solution:
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        graph = defaultdict(list)
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)

        print("Adjacency List of the Graph:")
        for key, value in graph.items():
            print(f"{key}: {value}")

        def dfs(node):
            for neighbor in graph[node]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    dfs(neighbor)

        seen = set()
        ans = 0
        for i in range(n):
            if i not in seen:
                ans += 1
                seen.add(i)
                dfs(i)

        return ans


def main():
    n = 5
    edges = [[0, 1], [1, 2], [3, 4]]
    print(Solution().countComponents(n, edges))


if __name__ == '__main__':
    main()