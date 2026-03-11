from typing import List

from collections import defaultdict


class Solution:
    def findCircleNum(self, isConnected: List[List[int]]) -> int:
        """input: adjacency matrix
                    city0  city1  city2
            city0  [1,    1,    0]   → city0 connected to city1
            city1  [1,    1,    0]   → city1 connected to city0
            city2  [0,    0,    1]   → city2 alone


        i=0, j=1: isConnected[0][1] = 1  ← city0-city1 connected
        i=0, j=2: isConnected[0][2] = 0  ← not connected
        i=1, j=2: isConnected[1][2] = 0  ← not connected

        """
        # build the graph
        n = len(isConnected)
        graph = defaultdict(list)
        for i in range(n):
            for j in range(i + 1, n):
                if isConnected[i][j]:
                    graph[i].append(j)
                    graph[j].append(i)
        print(graph)

        visited = set()

        def dfs(node):
            if node in visited:
                return
            visited.add(node)
            for neighbor in graph[node]:
                dfs(neighbor)

        count = 0
        for i in range(n):
            if i not in visited:
                dfs(i)
                count += 1

        return count


if __name__ == "__main__":
    sol = Solution()
    isConnected = [[1, 1, 0], [1, 1, 0], [0, 0, 1]]
    print(sol.findCircleNum(isConnected))
