from collections import deque
from typing import List, Tuple, Optional


class Solution:
    def shortestPathBinaryMatrix(self, grid: List[List[int]]) -> int:
        n = len(grid)
        if n == 0 or grid[0][0] != 0 or grid[n - 1][n - 1] != 0:
            return []

        # Each queue entry is (row, col, path_so_far)
        q = deque([(0, 0, [(0, 0)])])  # r,c, path
        # Mark visited by setting grid cell to 1
        grid[0][0] = 1

        directions = [[1, 0], [0, 1], [-1, 0], [0, -1], [1, 1], [-1, -1], [1, -1], [-1, 1]]

        while q:
            r, c, path = q.popleft()

            # If we reached the bottom‐right, return the accumulated path
            if (r, c) == (n - 1, n - 1):
                return path

            # Otherwise, explore all 8 neighbors
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0:
                    # mark visited immediately so we don't revisit
                    grid[nr][nc] = 1
                    # copy the path, append this neighbor, enqueue
                    new_path = path + [(nr, nc)]
                    q.append((nr, nc, new_path))
        return []


if __name__ == "__main__":
    grid = [[0, 0, 0], [1, 1, 0], [1, 1, 0]]
    print(Solution().shortestPathBinaryMatrix(grid))
