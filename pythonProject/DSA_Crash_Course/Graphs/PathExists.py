from collections import defaultdict
from typing import List


class Solution:
    def validPath(self, n: int, edges: List[List[int]], source: int, destination: int) -> bool:
        graph = defaultdict(list)
        for x, y in edges:
            graph[x].append(y)
            graph[y].append(x)

        print("Adjacency List of the Graph:")
        for key, value in graph.items():
            print(f"{key}: {value}")

        def dfs(node):
            for neighbor in graph[node]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    dfs(neighbor)

        seen = {source}
        dfs(source)
        return destination in seen


def main():
    n = 3
    edges = [[0, 1], [1, 2], [2, 0]]
    source = 0
    destination = 2
    print(Solution().validPath(n, edges, source, destination))
    n = 6
    edges = [[0, 1], [0, 2], [3, 5], [5, 4], [4, 3]]
    source = 0
    destination = 5
    print(Solution().validPath(n, edges, source, destination))
    n = 10
    edges = [[4, 3], [1, 4], [4, 8], [1, 7], [6, 4], [4, 2], [7, 4], [4, 0], [0, 9], [5, 4]]
    source = 5
    destination = 9
    print(Solution().validPath(n, edges, source, destination))


if __name__ == '__main__':
    main()
