from collections import deque
from typing import List


class Solution:
    def shortestPathBinaryMatrix(self, grid: List[List[int]]) -> int:
        n = len(grid)
        q = deque([(0, 0, 1)])  # r,c,length(=steps)
        visit = set((0, 0))

        directions = [[1, 0], [0, 1], [-1, 0], [0, -1], [1, 1], [-1, -1], [1, -1], [-1, 1]]

        while q:
            r, c, steps = q.popleft()
            if min(r, c) < 0 or max(r, c) >= n or grid[r][c] == 1:
                continue
            if r == n - 1 and c == n - 1:
                return steps
            for dr, dc in directions:
                if (r + dr, c + dc) not in visit:
                    q.append((r + dr, c + dc, steps + 1))
                    visit.add((r + dr, c + dc))
        return -1


if __name__ == "__main__":
    grid = [[0, 0, 0], [1, 1, 0], [1, 1, 0]]
    print(Solution().shortestPathBinaryMatrix(grid))
