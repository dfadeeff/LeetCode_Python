from typing import List

from collections import defaultdict


class Solution:
    def findCircleNum(self, isConnected: List[List[int]]) -> int:
        # build graph
        n = len(isConnected)
        graph = defaultdict(list)
        for i in range(n):
            for j in range(i + 1, n):
                if isConnected[i][j]:
                    graph[i].append(j)
                    graph[j].append(i)

        print(graph)

        # count provinces using DFS
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
    isConnected = [[1, 1, 0], [1, 1, 0], [0, 0, 1]]
    print(sol.findCircleNum(isConnected))
