from typing import List


class Solution:
    def numDistinctIslands(self, grid: List[List[int]]) -> int:
        def dfs(row, col, r0, c0, shape):
            for dr, dc in directions:
                nr, nc = row + dr, col + dc
                if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 1 and (nr, nc) not in seen:
                    seen.add((nr, nc))
                    shape.append((nr - r0, nc - c0))  # relative position
                    dfs(nr, nc, r0, c0, shape)

        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        seen = set()
        unique_shapes = set()
        m, n = len(grid), len(grid[0])

        for r in range(m):
            for c in range(n):
                if grid[r][c] == 1 and (r, c) not in seen:
                    shape = []
                    seen.add((r, c))
                    shape.append((0, 0))  # relative origin
                    dfs(r, c, r, c, shape)
                    unique_shapes.add(tuple(shape))  # convert list to tuple for set

        return len(unique_shapes)


if __name__ == "__main__":
    grid = [[1, 1, 0, 0, 0], [1, 1, 0, 0, 0], [0, 0, 0, 1, 1], [0, 0, 0, 1, 1]]
    print(Solution().numDistinctIslands(grid))
