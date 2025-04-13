from typing import List


class Solution:
    def updateBoard(self, board: List[List[str]], click: List[int]) -> List[List[str]]:
        rows, cols = len(board), len(board[0])

        def count_mines(r, c):
            count = 0
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == 'M':
                    count += 1
            return count

        def dfs(r, c):
            if not (0 <= r < rows and 0 <= c < cols):
                return
            if board[r][c] != 'E':
                return

            mines = count_mines(r, c)
            if mines > 0:
                board[r][c] = str(mines)
            else:
                board[r][c] = 'B'
                for dr, dc in directions:
                    dfs(r + dr, c + dc)

        click_r, click_c = click
        if board[click_r][click_c] == 'M':
            board[click_r][click_c] = 'X'
        else:
            directions = [(-1, -1), (-1, 0), (-1, 1),
                          (0, -1), (0, 1),
                          (1, -1), (1, 0), (1, 1)]
            dfs(click_r, click_c)

        return board


if __name__ == "__main__":
    board = [["E", "E", "E", "E", "E"], ["E", "E", "M", "E", "E"], ["E", "E", "E", "E", "E"],
             ["E", "E", "E", "E", "E"]]
    click = [3, 0]
    print(Solution().updateBoard(board, click))
