from collections import deque
from typing import List


class Solution:
    def shortestDistanceSteps(self, maze: List[List[int]], start: List[int], destination: List[int]) -> int:
        m, n = len(maze), len(maze[0])
        seen = {(start[0], start[1])}
        queue = deque([(start[0], start[1], 1)])  # row, col, steps
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        while queue:
            row, col, steps = queue.popleft()
            if [row, col] == destination:
                return steps
            for dr, dc in directions:
                r, c = row, col
                while 0 <= r + dr < m and 0 <= c + dc < n and maze[r + dr][c + dc] == 0:
                    r += dr
                    c += dc
                if (r, c) not in seen:
                    seen.add((r, c))
                    queue.append((r, c, steps + 1))

        return -1


    def shortestDistance(self, maze: List[List[int]], start: List[int], destination: List[int]) -> int:
        m, n = len(maze), len(maze[0])
        distance = [[float('inf')] * n for _ in range(m)]
        distance[start[0]][start[1]] = 0
        queue = deque([(start[0], start[1])])
        directions = [(0, 1), (0, -1), (-1, 0), (1, 0)]

        while queue:
            row, col = queue.popleft()

            for dr, dc in directions:
                r, c = row, col
                steps = 0

                # Roll the ball until it hits a wall
                while 0 <= r + dr < m and 0 <= c + dc < n and maze[r + dr][c + dc] == 0:
                    r += dr
                    c += dc
                    steps += 1

                # Check if this new path is shorter
                if distance[row][col] + steps < distance[r][c]:
                    distance[r][c] = distance[row][col] + steps
                    queue.append((r, c))

        result = distance[destination[0]][destination[1]]
        return -1 if result == float('inf') else result


if __name__ == '__main__':
    maze = [[0, 0, 1, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 1, 0], [1, 1, 0, 1, 1], [0, 0, 0, 0, 0]]
    start = [0, 4]
    destination = [4, 4]
    print(Solution().shortestDistance(maze, start, destination))
