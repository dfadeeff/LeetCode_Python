from collections import deque
from typing import List


class Solution:
    def shortestDistance(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        total_buildings = sum(val == 1 for row in grid for val in row)
        distances = [[0] * n for _ in range(m)]
        reach_count = [[0] * n for _ in range(m)]

        def bfs(start_row, start_col):
            visited = [[False] * n for _ in range(m)]
            queue = deque([(start_row, start_col, 0)])  # (row, col, distance)
            visited[start_row][start_col] = True
            while queue:
                row, col, dist = queue.popleft()
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    r, c = row + dr, col + dc

                    if 0 <= r < m and 0 <= c < n and not visited[r][c] and grid[r][c] == 0:
                        visited[r][c] = True
                        distances[r][c] += dist + 1
                        reach_count[r][c] += 1
                        queue.append((r, c, dist + 1))

        # Step 1: Run BFS from every building
        for row in range(m):
            for col in range(n):
                if grid[row][col] == 1:
                    bfs(row, col)

        # Step 2: Find minimum distance
        answer = float('inf')
        for row in range(m):
            for col in range(n):
                if grid[row][col] == 0 and reach_count[row][col] == total_buildings:
                    answer = min(answer, distances[row][col])

        return answer if answer != float('inf') else -1


if __name__ == "__main__":
    grid = [[1, 0, 2, 0, 1], [0, 0, 0, 0, 0], [0, 0, 1, 0, 0]]
    print(Solution().shortestDistance(grid))
