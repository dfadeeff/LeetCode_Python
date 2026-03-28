from typing import List


class Solution:
    def earliestAcq(self, logs: List[List[int]], n: int) -> int:
        logs.sort()
        parent = list(range(n))
        rank = [0] * n
        count = n  # n separate people

        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])

            return parent[x]

        def union(a, b):
            nonlocal count
            ra, rb = find(a), find(b)
            if ra == rb:
                return
            if rank[ra] < rank[rb]:
                ra, rb = rb, ra
            parent[rb] = ra
            if rank[ra] == rank[rb]:
                rank[ra] += 1
            count -= 1

        for time, a, b in logs:
            union(a, b)
            if count == 1:  # all connected!
                return time

        return -1


if __name__ == "__main__":
    sol = Solution()
    logs = [[20190101, 0, 1], [20190104, 3, 4], [20190107, 2, 3], [20190211, 1, 5], [20190224, 2, 4], [20190301, 0, 3],
            [20190312, 1, 2], [20190322, 4, 5]]
    n = 6
    print(sol.earliestAcq(logs, n))
