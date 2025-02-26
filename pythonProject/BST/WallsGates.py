from collections import deque
from typing import List


class Solution:
    def wallsAndGates(self, rooms: List[List[int]]) -> None:
        """
        Do not return anything, modify rooms in-place instead.
        """
        if not rooms or not rooms[0]:
            return
        rows = len(rooms)
        cols = len(rooms[0])
        queue = deque()
        INF = 2147483647
        for i in range(rows):
            for j in range(cols):
                if rooms[i][j] == 0:
                    queue.append((i, j))
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        while queue:
            r, c = queue.popleft()
            for dr, dc in directions:
                new_dr, new_dc = r + dr, c + dc
                if 0 <= new_dr < rows and 0 <= new_dc < cols and rooms[new_dr][new_dc] == INF:
                    rooms[new_dr][new_dc] = rooms[r][c] + 1
                    queue.append((new_dr, new_dc))


if __name__ == '__main__':
    rooms = [[2147483647, -1, 0, 2147483647], [2147483647, 2147483647, 2147483647, -1],
             [2147483647, -1, 2147483647, -1], [0, -1, 2147483647, 2147483647]]
    print(Solution().wallsAndGates(rooms))
