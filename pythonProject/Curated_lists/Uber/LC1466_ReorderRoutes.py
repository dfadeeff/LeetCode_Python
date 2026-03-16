from typing import List

from collections import defaultdict


class Solution:
    def minReorder(self, n: int, connections: List[List[int]]) -> int:
        roads = set()
        graph = defaultdict(list)
        for x_from, y_to in connections:
            graph[x_from].append(y_to)
            graph[y_to].append(x_from)
            roads.add((x_from, y_to))

        print(graph)

        def dfs(node):
            ans = 0
            for neighbor in graph[node]:
                if neighbor not in seen:
                    if (node, neighbor) in roads:
                        ans += 1
                    seen.add(neighbor)
                    ans += dfs(neighbor)

            return ans

        seen = {0}
        return dfs(0)


if __name__ == "__main__":
    sol = Solution()
    n = 6
    connections = [[0, 1], [1, 3], [2, 3], [4, 0], [4, 5]]
    print(sol.minReorder(n, connections))
