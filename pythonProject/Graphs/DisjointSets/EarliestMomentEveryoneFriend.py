from collections import defaultdict
from typing import List


class Solution:
    def earliestAcq(self, logs: List[List[int]], n: int) -> int:
        # Sort logs by timestamp
        logs.sort()

        # DSU / Union Find
        parent = [i for i in range(n)]
        components = n  # initially, n disconnected components

        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])  # path compression
            return parent[x]

        def union(x, y):
            nonlocal components
            root_x, root_y = find(x), find(y)
            if root_x != root_y:
                parent[root_x] = root_y
                components -= 1
                return True
            return False

        for timestamp, u, v in logs:
            union(u, v)
            if components == 1:
                return timestamp
        return -1  # not all connected


if __name__ == '__main__':
    logs = [[20190101, 0, 1], [20190104, 3, 4], [20190107, 2, 3], [20190211, 1, 5], [20190224, 2, 4], [20190301, 0, 3],
            [20190312, 1, 2], [20190322, 4, 5]]
    n = 6
    print(Solution().earliestAcq(logs, n))
