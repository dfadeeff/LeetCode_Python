from collections import deque
from heapq import heappush, heappop
from typing import List


class Solution:
    def findShortestWay(self, maze: List[List[int]], ball: List[int], hole: List[int]) -> str:
        m, n = len(maze), len(maze[0])
        directions = [(-1, 0, 'u'), (1, 0, 'd'), (0, -1, 'l'), (0, 1, 'r')]
        dist_map = {}
        queue = deque([(ball[0], ball[1], 0, "")])  # (row, col, steps, path)

        while queue:
            row, col, dist, path = queue.popleft()

            # If this cell has a better path before, skip it
            if (row, col) in dist_map:
                prev_dist, prev_path = dist_map[(row, col)]
                if dist > prev_dist or (dist == prev_dist and path >= prev_path):
                    continue

            dist_map[(row, col)] = (dist, path)

            for dr, dc, dir_char in directions:
                r, c = row, col
                steps = 0
                while 0 <= r + dr < m and 0 <= c + dc < n and maze[r + dr][c + dc] == 0:
                    r += dr
                    c += dc
                    steps += 1
                    if [r, c] == hole:
                        break
                # Only add to queue if it's a better path
                if (r, c) not in dist_map or dist + steps < dist_map[(r, c)][0] or (
                        dist + steps == dist_map[(r, c)][0] and path + dir_char < dist_map[(r, c)][1]):
                    queue.append((r, c, dist + steps, path + dir_char))

        return dist_map.get((hole[0], hole[1]), (None, "impossible"))[1]


if __name__ == '__main__':
    maze = [[0, 0, 0, 0, 0], [1, 1, 0, 0, 1], [0, 0, 0, 0, 0], [0, 1, 0, 0, 1], [0, 1, 0, 0, 0]]
    ball = [4, 3]
    hole = [0, 1]
    print(Solution().findShortestWay(maze, ball, hole))
