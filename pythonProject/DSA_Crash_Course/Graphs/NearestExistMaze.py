from collections import deque
from typing import List


class Solution:
    def nearestExit(self, maze: List[List[str]], entrance: List[int]) -> int:
        # Dimensions of the maze
        n = len(maze)  # Number of rows
        m = len(maze[0])  # Number of columns

        # Helper function to check if a cell is valid for movement
        def valid(row, col):
            return 0 <= row < n and 0 <= col < m and maze[row][col] == "."

        queue = deque()
        entrance_row, entrance_col = entrance
        queue.append((entrance_row, entrance_col, 1))  # (row, col, steps)
        seen = {(entrance_row, entrance_col)}
        # Directions: Right, Down, Left, Up
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        while queue:
            row, col, steps = queue.popleft()

            for dx, dy in directions:
                next_row, next_col = row + dy, col + dx

                is_border = next_row == 0 or next_row == n - 1 or next_col == 0 or next_col == m - 1
                if valid(next_row, next_col) and is_border and (next_row, next_col) != (entrance_row, entrance_col):
                    return steps

                if valid(next_row, next_col) and (next_row, next_col) not in seen:
                    seen.add((next_row, next_col))
                    queue.append((next_row, next_col, steps + 1))

        return -1


def main():
    maze = [["+", "+", ".", "+"], [".", ".", ".", "+"], ["+", "+", "+", "."]]
    entrance = [1, 2]
    print(Solution().nearestExit(maze, entrance))
    maze = [["+", "+", "+"], [".", ".", "."], ["+", "+", "+"]]
    entrance = [1, 0]
    print(Solution().nearestExit(maze, entrance))
    maze = [[".", "+"]]
    entrance = [0, 0]
    print(Solution().nearestExit(maze, entrance))


if __name__ == '__main__':
    main()
