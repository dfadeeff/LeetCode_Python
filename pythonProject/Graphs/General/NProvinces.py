from collections import defaultdict
from typing import List


class Solution:
    def findCircleNum(self, isConnected: List[List[int]]) -> int:
        n = len(isConnected)
        graph = defaultdict(list)
        for i in range(n):
            for j in range(i + 1, n):
                if isConnected[i][j]:
                    graph[i].append(j)
                    graph[j].append(i)
        print(graph)

        def dfs(node):
            for neighbor in graph[node]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    dfs(neighbor)

        seen = set()
        ans = 0
        for i in range(n):
            if i not in seen:
                seen.add(i)
                ans += 1
                dfs(i)
        return ans


if __name__ == '__main__':
    isConnected = [[1, 1, 0], [1, 1, 0], [0, 0, 1]]
    print(Solution().findCircleNum(isConnected))
