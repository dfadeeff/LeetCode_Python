from collections import defaultdict
from typing import List


class Solution:
    def validPath(self, n: int, edges: List[List[int]], source: int, destination: int) -> bool:
        graph = defaultdict(list)
        for x,y in edges:
            graph[x].append(y)
            graph[y].append(x)

        def dfs(source):
            if source == destination:
                return True
            for neighbor in graph[source]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    dfs(neighbor)
            return destination in seen
        seen = set()
        return dfs(source)




if __name__ == '__main__':
    n = 3
    edges = [[0, 1], [1, 2], [2, 0]]
    source = 0
    destination = 2
    print(Solution().validPath(n, edges, source, destination))
