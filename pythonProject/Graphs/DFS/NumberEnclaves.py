from typing import List


class Solution:
    def numEnclaves(self, grid: List[List[int]]) -> int:
        if not grid:
            return 0

        rows, cols = len(grid), len(grid[0])

        def dfs(r, c):
            if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != 1:
                return 0
            grid[r][c] = 'E'
            dfs(r + 1, c)
            dfs(r - 1, c)
            dfs(r, c + 1)
            dfs(r, c - 1)

        # 1. Mark border-connected '1's
        for r in range(rows):
            for c in [0, cols - 1]:
                dfs(r, c)
        for c in range(cols):
            for r in [0, rows - 1]:
                dfs(r, c)

        ans = 0
        # 2. Flip surrounded and escaped regions
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 1:
                    ans += 1

        return ans


if __name__ == "__main__":
    grid = [[0, 0, 0, 0], [1, 0, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0]]
    print(Solution().numEnclaves(grid))
    grid = [[0, 1, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 0, 0]]
    print(Solution().numEnclaves(grid))
