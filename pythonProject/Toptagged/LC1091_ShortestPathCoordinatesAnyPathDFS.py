from collections import deque
from typing import List, Tuple, Optional


class Solution:
    def shortestPathBinaryMatrix(self, grid: List[List[int]]) -> int:
        n = len(grid)
        # Quick checks: empty grid or start/end blocked
        if n == 0 or grid[0][0] != 0 or grid[n - 1][n - 1] != 0:
            return []

        # All 8 directions: N, NE, E, SE, S, SW, W, NW
        directions = [
            (-1, 0), (-1, 1), (0, 1), (1, 1),
            (1, 0), (1, -1), (0, -1), (-1, -1),
        ]

        path = []

        def dfs(r: int, c: int) -> bool:
            # mark visited
            grid[r][c] = 1
            path.append([r, c])

            # if we’ve reached the goal, stop
            if (r, c) == (n - 1, n - 1):
                return True

            # try all 8 neighbors
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0:
                    if dfs(nr, nc):
                        return True

            # dead end — backtrack
            path.pop()
            return False

        # launch DFS from the top‐left
        dfs(0, 0)
        return path


if __name__ == "__main__":
    grid = [[0, 0, 0], [1, 1, 0], [1, 1, 0]]
    print(Solution().shortestPathBinaryMatrix(grid))
