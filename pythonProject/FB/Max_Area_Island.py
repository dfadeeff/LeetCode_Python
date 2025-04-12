from typing import List


class Solution:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        def valid(row, col):
            return 0 <= row < m and 0 <= col < n and grid[row][col] == 1

        def dfs(row, col):
            area = 1
            for dr, dc in directions:
                print("dr: ", dr, "dc: ", dc)
                next_row, next_col = row + dr, col + dc
                if valid(next_row, next_col) and (next_row, next_col) not in seen:
                    seen.add((next_row, next_col))
                    area += dfs(next_row, next_col)
            return area

        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        seen = set()

        m = len(grid)
        n = len(grid[0])
        max_area = 0
        for row in range(m):
            for col in range(n):
                if grid[row][col] == 1 and (row, col) not in seen:
                    seen.add((row, col))
                    current_area = dfs(row, col)
                    max_area = max(current_area, max_area)

        return max_area

if __name__ == '__main__':
    grid = [[0,0,1,0,0,0,0,1,0,0,0,0,0],[0,0,0,0,0,0,0,1,1,1,0,0,0],[0,1,1,0,1,0,0,0,0,0,0,0,0],[0,1,0,0,1,1,0,0,1,0,1,0,0],[0,1,0,0,1,1,0,0,1,1,1,0,0],[0,0,0,0,0,0,0,0,0,0,1,0,0],[0,0,0,0,0,0,0,1,1,1,0,0,0],[0,0,0,0,0,0,0,1,1,0,0,0,0]]
    print(Solution().maxAreaOfIsland(grid))