from collections import deque
from typing import List, Tuple, Optional


class Solution:
    def shortestPathBinaryMatrix(self, grid: List[List[int]]) -> int:
        n = len(grid)
        if n == 0 or grid[0][0] != 0 or grid[n - 1][n - 1] != 0:
            return []

        q = deque([(0, 0)])  # r,c
        # parent[(r,c)] = (pr,pc) or None for the start
        parent: dict[Tuple[int, int], Optional[Tuple[int, int]]] = {(0, 0): None}

        visit = set((0, 0))

        directions = [[1, 0], [0, 1], [-1, 0], [0, -1], [1, 1], [-1, -1], [1, -1], [-1, 1]]

        while q:
            r, c = q.popleft()
            if (r, c) == (n - 1, n - 1):
                # reconstruct path
                path = []
                cur = (n - 1, n - 1)
                while cur is not None:
                    path.append(cur)
                    cur = parent[cur]
                return path[::-1]  # reverse to go from (0,0) → (n-1,n-1)

            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0:
                    if (nr, nc) not in parent:
                        parent[(nr, nc)] = (r, c)
                        q.append((nr, nc))

        return []


if __name__ == "__main__":
    grid = [[0, 0, 0], [1, 1, 0], [1, 1, 0]]
    print(Solution().shortestPathBinaryMatrix(grid))
