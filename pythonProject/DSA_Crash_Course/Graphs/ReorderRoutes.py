from collections import defaultdict
from typing import List


class Solution:
    def minReorder(self, n: int, connections: List[List[int]]) -> int:
        # analog to seen
        roads = set()
        graph = defaultdict(list)
        for x, y in connections:
            graph[x].append(y)
            graph[y].append(x)
            roads.add((x, y))

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


def main():
    n = 6
    connections = [[0, 1], [1, 3], [2, 3], [4, 0], [4, 5]]
    print(Solution().minReorder(n, connections))


if __name__ == '__main__':
    main()
