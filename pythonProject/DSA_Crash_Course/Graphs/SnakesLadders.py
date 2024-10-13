from collections import deque
from typing import List


class Solution:
    def snakesAndLadders(self, board: List[List[int]]) -> int:
        n = len(board)

        def num_to_pos(s: int) -> (int, int):
            quot, rem = divmod(s - 1, n)
            row = n - 1 - quot
            if quot % 2 == 0:
                col = rem
            else:
                col = n - 1 - rem
            return row, col

        visited = set()
        queue = deque()

        # Start from square 1 with 0 moves
        queue.append((1, 0))
        visited.add(1)

        while queue:
            current, steps = queue.popleft()

            # If we've reached the last square, return the steps taken
            if current == n * n:
                return steps

            # Try all possible moves from 1 to 6
            for move in range(1, 7):
                next_sq = current + move
                if next_sq > n * n:
                    continue  # Skip squares beyond the board

                row, col = num_to_pos(next_sq)

                # If there's a snake or ladder, jump to its destination
                if board[row][col] != -1:
                    next_sq = board[row][col]

                if next_sq == n * n:
                    return steps + 1  # Reached the end

                if next_sq not in visited:
                    visited.add(next_sq)
                    queue.append((next_sq, steps + 1))

        # If we exit the loop without returning, there's no path
        return -1


def main():
    board = [[-1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1], [-1, 35, -1, -1, 13, -1],
             [-1, -1, -1, -1, -1, -1], [-1, 15, -1, -1, -1, -1]]
    print(Solution().snakesAndLadders(board))


if __name__ == '__main__':
    main()
