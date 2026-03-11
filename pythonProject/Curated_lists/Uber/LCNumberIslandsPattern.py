from typing import List


class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        m, n = len(grid), len(grid[0])
        seen = set()

        def dfs(r, c):
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                new_dr, new_dc = r + dr, c + dc
                if 0 <= new_dr < m and 0 <= new_dc < n and grid[new_dr][new_dc] == "1" and (new_dr, new_dc) not in seen:
                    seen.add((new_dr, new_dc))
                    dfs(new_dr, new_dc)

        count = 0
        for r in range(m):
            for c in range(n):
                if grid[r][c] == "1" and (r, c) not in seen:
                    seen.add((r, c))
                    dfs(r, c)
                    count += 1
        return count


if __name__ == "__main__":
    sol = Solution()
    grid = [
        ["1", "1", "1", "1", "0"],
        ["1", "1", "0", "1", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "0", "0", "0"]
    ]
    print(sol.numIslands(grid))
