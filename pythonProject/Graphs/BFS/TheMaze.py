from collections import deque
from typing import List


class Solution:
    def hasPath(self, maze: List[List[int]], start: List[int], destination: List[int]) -> bool:


        def valid(row, col):
            return 0 <= row < m and 0 <= col < n and maze[row][col] == 0

        m, n = len(maze), len(maze[0])
        seen = {(start[0], start[1])}
        queue = deque([(start[0], start[1])])  # row, col, steps
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        while queue:
            row, col = queue.popleft()
            if [row, col] == destination:
                return True
            for dx, dy in directions:
                x, y = row, col
                # Roll the ball in the current direction until it hits a wall
                while 0 <= x + dy < m and 0 <= y + dx < n and maze[x + dy][y + dx] == 0:
                    x += dy
                    y += dx

                if (x, y) not in seen:
                    seen.add((x, y))
                    queue.append((x, y))

        return False


if __name__ == "__main__":
    maze = [[0, 0, 1, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 1, 0], [1, 1, 0, 1, 1], [0, 0, 0, 0, 0]]
    start = [0, 4]
    destination = [4, 4]
    print(Solution().hasPath(maze, start, destination))
    maze = [[0, 0, 1, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 1, 0], [1, 1, 0, 1, 1], [0, 0, 0, 0, 0]]
    start = [0, 4]
    destination = [3, 2]
    print(Solution().hasPath(maze, start, destination))
