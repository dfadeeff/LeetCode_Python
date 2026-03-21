import heapq
from typing import List


class Solution:
    def minimumEffortPath(self, heights: List[List[int]]) -> int:
        m, n = len(heights), len(heights[0])
        DIRS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        dist = {}
        pq = [(0, 0, 0)]  # (effort, row, col)
        while pq:
            effort, r, c = heapq.heappop(pq)

            if (r, c) in dist:
                continue
            dist[(r, c)] = effort
            if r == m - 1 and c == n - 1:
                return effort

            for dr, dc in DIRS:
                nr, nc = r + dr, c + dc
                if (0 <= nr < m and 0 <= nc < n and (nr, nc) not in dist):
                    new_effort = max(effort, abs(heights[nr][nc] - heights[r][c]))
                    heapq.heappush(pq, (new_effort, nr, nc))
        return 0

if __name__ == "__main__":
    sol = Solution()
    heights = [[1, 2, 3], [3, 8, 4], [5, 3, 5]]
    print(sol.minimumEffortPath(heights))
