from collections import deque
from typing import List


class Solution:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:

        """
        The pattern — "BFS from multiple sources"
        # Single source BFS
        queue = deque([start])
        visited = {start}

        # Multi-source BFS
        queue = deque(all_borders)
        visited = set(all_borders)


        """
        if not heights:
            return []

        m, n = len(heights), len(heights[0])
        DIRS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        def bfs(starts):
            visited = set(starts)
            queue = deque(starts)

            while queue:
                r, c = queue.popleft()
                for dr, dc in DIRS:
                    nr, nc = r + dr, c + dc
                    if (0 <= nr < m and 0 <= nc < n) and (nr, nc) not in visited and heights[nr][nc] >= heights[r][
                        c]:  # uphill
                        visited.add((nr, nc))
                        queue.append((nr, nc))
            return visited

        # seed border cells for each ocean
        pacific_starts = [(0, c) for c in range(n)] + [(r, 0) for r in range(1, m)]
        atlantic_starts = [(m - 1, c) for c in range(n)] + [(r, n - 1) for r in range(m - 1)]

        pacific = bfs(pacific_starts)
        atlantic = bfs(atlantic_starts)

        # intersection = flows to both
        return [[r, c] for r, c in pacific & atlantic]


if __name__ == "__main__":
    sol = Solution()
    heights = [[1, 2, 2, 3, 5], [3, 2, 3, 4, 4], [2, 4, 5, 3, 1], [6, 7, 1, 4, 5], [5, 1, 1, 2, 4]]
    print(sol.pacificAtlantic(heights))
