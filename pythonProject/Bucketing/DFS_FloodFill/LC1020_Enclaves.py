from typing import List


class Solution:
    def numEnclaves(self, grid: List[List[int]]) -> int:
        """The problem says: count land cells that cannot reach the border.

        start 1: border land cells      → mark everything reachable from border
        start 2: everything else        → count remaining unvisited land

        That's why you need 2 passes. The first pass is not counting — it's elimination. The second pass counts survivors.

        """
        rows, cols = len(grid), len(grid[0])
        seen = set()

        def dfs(r, c):
            if r < 0 or r >= rows or c < 0 or c >= cols:
                return
            if grid[r][c] == 0 or (r, c) in seen:
                return
            seen.add((r, c))
            dfs(r + 1, c)
            dfs(r - 1, c)
            dfs(r, c + 1)
            dfs(r, c - 1)

        # Pass 1: sink all islands touching the border
        for r in range(rows):
            for c in range(cols):
                if (r == 0 or r == rows - 1 or c == 0 or c == cols - 1):
                    if grid[r][c] == 1:
                        dfs(r, c)

        # Pass 2: count what's left
        count = 0
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 1 and (r, c) not in seen:
                    count += 1

        return count


if __name__ == "__main__":
    sol = Solution()
    grid = [[0, 0, 0, 0], [1, 0, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0]]
    print(sol.numEnclaves(grid))
