from collections import deque
from typing import List


class Solution:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        if not heights or not heights[0]:
            return []

        m, n = len(heights), len(heights[0])
        # reachable_p[i][j] True if (i,j) can reach Pacific
        # reachable_a[i][j] True if (i,j) can reach Atlantic
        reachable_p = [[False] * n for _ in range(m)]
        reachable_a = [[False] * n for _ in range(m)]

        def bfs(starts, reachable):
            queue = deque(starts)
            for x, y in starts:
                reachable[x][y] = True

            while queue:
                x, y = queue.popleft()
                for dx, dy in ((1, 0), (-1, 0), (0, -1), (0, 1)):
                    new_row, new_col = x + dx, y + dy

                    if (0 <= new_row < m and 0 <= new_col < n and not reachable[new_row][new_col]
                            and heights[new_row][new_col] >= heights[x][y]):
                        reachable[new_row][new_col] = True
                        queue.append((new_row, new_col))

        pacific_starts = [(0, j) for j in range(n)] + [(i, 0) for i in range(m)]
        atlantic_starts = [(m - 1, j) for j in range(n)] + [(i, n - 1) for i in range(m)]

        bfs(pacific_starts, reachable_p)
        bfs(atlantic_starts, reachable_a)

        result = []
        for i in range(m):
            for j in range(n):
                if reachable_p[i][j] and reachable_a[i][j]:
                    result.append([i, j])

        return result


if __name__ == "__main__":
    heights = [[1, 2, 2, 3, 5], [3, 2, 3, 4, 4], [2, 4, 5, 3, 1], [6, 7, 1, 4, 5], [5, 1, 1, 2, 4]]
    print(Solution().pacificAtlantic(heights))
