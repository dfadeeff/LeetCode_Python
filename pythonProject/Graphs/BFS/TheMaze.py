from collections import deque
from typing import List


class Solution:
    def hasPath(self, maze: List[List[int]], start: List[int], destination: List[int]) -> bool:

        m, n = len(maze), len(maze[0])
        seen = {(start[0], start[1])}
        queue = deque([(start[0], start[1])])  # row, col, steps
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        while queue:
            row, col = queue.popleft()
            if [row, col] == destination:
                return True
            for dr, dc in directions:
                r, c = row, col  # start from current position
                while 0 <= r + dr < m and 0 <= c + dc < n and maze[r + dr][c + dc] == 0:
                    r += dr
                    c += dc
                if (r, c) not in seen:
                    seen.add((r, c))
                    queue.append((r, c))

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
