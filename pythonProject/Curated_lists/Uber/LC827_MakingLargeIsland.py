from typing import List


class Solution:
    def largestIsland(self, grid: List[List[int]]) -> int:
        n = len(grid)
        island_id = 2  # start at 2 (0 and 1 already used)
        island_size = {}

        # ---- PASS 1: Same as Number of Islands, but label + measure ----
        def dfs(r, c, label):
            if r < 0 or r >= n or c < 0 or c >= n:
                return 0
            if grid[r][c] != 1:  # not unvisited land
                return 0
            grid[r][c] = label
            return 1 + dfs(r + 1, c, label) + dfs(r - 1, c, label) + dfs(r, c + 1, label) + dfs(r, c - 1, label)

        for r in range(n):
            for c in range(n):
                if grid[r][c] == 1:
                    island_size[island_id] = dfs(r, c, island_id)
                    island_id += 1

        # ---- EDGE CASE: no 0s to flip (all land) ----
        if not island_size:
            return 1  # all 0s → flip one → size 1

        result = max(island_size.values())  # best without flipping

        # ---- PASS 2: Try flipping each 0 ----
        for r in range(n):
            for c in range(n):
                if grid[r][c] == 0:
                    # Collect DISTINCT neighbor islands
                    neighbor_islands = set()
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] > 1:
                            neighbor_islands.add(grid[nr][nc])

                    # Size = 1 (flipped cell) + all neighbor island sizes
                    total = 1
                    for island in neighbor_islands:
                        total += island_size[island]

                    result = max(result, total)

        return result

if __name__ == "__main__":
    sol = Solution()

    grid = [[1, 1], [1, 0]]
    print(sol.largestIsland(grid))

