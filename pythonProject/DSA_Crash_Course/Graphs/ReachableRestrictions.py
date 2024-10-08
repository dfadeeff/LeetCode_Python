from collections import defaultdict
from typing import List


class Solution:
    def reachableNodes(self, n: int, edges: List[List[int]], restricted: List[int]) -> int:

        restricted_set = set(restricted)

        graph = defaultdict(list)
        for x, y in edges:
            graph[x].append(y)
            graph[y].append(x)

        def dfs(node):
            for neighbor in graph[node]:
                if neighbor not in seen and neighbor not in restricted_set:
                    seen.add(neighbor)
                    dfs(neighbor)

        seen = {0}
        dfs(0)
        return len(seen)


def main():
    n = 7
    edges = [[0, 1], [1, 2], [3, 1], [4, 0], [0, 5], [5, 6]]
    restricted = [4, 5]
    print(Solution().reachableNodes(n, edges, restricted))
    n = 7
    edges = [[0, 1], [0, 2], [0, 5], [0, 4], [3, 2], [6, 5]]
    restricted = [4, 2, 1]
    print(Solution().reachableNodes(n, edges, restricted))

if __name__ == '__main__':
    main()
