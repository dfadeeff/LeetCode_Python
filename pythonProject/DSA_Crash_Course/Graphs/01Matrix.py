from collections import deque
from typing import List


class Solution:
    def updateMatrix(self, mat: List[List[int]]) -> List[List[int]]:
        def valid(row, col):
            return 0 <= row < len(mat) and 0 <= col < len(mat[0])

        m = len(mat)
        n = len(mat[0])
        queue = deque()
        seen = set()

        for row in range(m):
            for col in range(n):
                if mat[row][col] == 0:
                    queue.append((row, col, 1))
                    seen.add((row, col))

        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        while queue:
            row, col, steps = queue.popleft()
            for dx, dy in directions:
                newrow, newcol = row + dx, col + dy
                if valid(newrow, newcol) and (newrow, newcol) not in seen:
                    seen.add((newrow, newcol))
                    queue.append((newrow, newcol, steps + 1))
                    mat[newrow][newcol] = steps

        return mat


def main():
    mat = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    print(Solution().updateMatrix(mat))
    mat = [[0, 0, 0], [0, 1, 0], [1, 1, 1]]
    print(Solution().updateMatrix(mat))

if __name__ == '__main__':
    main()
