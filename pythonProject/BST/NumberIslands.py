from collections import deque
from typing import List


class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        if not grid:
            return 0  # Edge case: empty grid

        rows, cols = len(grid), len(grid[0])
        num_islands = 0
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Down, Up, Right, Left

        def bfs(r, c):
            """Perform BFS to mark all parts of the island starting from (r, c)."""
            queue = deque([(r, c)])
            grid[r][c] = "0"  # Mark as visited

            while queue:
                size = len(queue)

                for _ in range(size):  # Process all nodes at the current level
                    row, col = queue.popleft()

                    for dr, dc in directions:
                        new_r, new_c = row + dr, col + dc

                        if 0 <= new_r < rows and 0 <= new_c < cols and grid[new_r][new_c] == "1":
                            grid[new_r][new_c] = "0"  # Mark as visited
                            queue.append((new_r, new_c))  # Add to queue

        # Step 1: Iterate through the grid
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == "1":  # Found a new island
                    num_islands += 1  # Increment island count
                    bfs(r, c)  # Perform BFS to mark the entire island

        return num_islands

if __name__ == '__main__':
    grid = [
        ["1", "1", "1", "1", "0"],
        ["1", "1", "0", "1", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "0", "0", "0"]
    ]

    print(Solution().numIslands(grid))