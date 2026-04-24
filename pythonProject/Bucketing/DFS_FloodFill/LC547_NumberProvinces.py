from typing import List
from collections import defaultdict


class Solution:

    def findCircleNum(self, isConnected: List[List[int]]) -> int:
        n = len(isConnected)
        graph = defaultdict(list)
        for i in range(n):
            # Why j = i + 1 and not j = 0?
            # The matrix is symmetric — isConnected[0][1] and isConnected[1][0] are the same

            for j in range(i + 1, n):
                if isConnected[i][j]:
                    graph[i].append(j)
                    graph[j].append(i)

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
