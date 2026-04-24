from typing import List


class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        rows, cols = len(board), len(board[0])
        seen = set()

        def dfs(r, c, i):
            if i == len(word):
                return True
            if r < 0 or r >= rows or c < 0 or c >= cols:
                return False
            if board[r][c] != word[i] or (r, c) in seen:
                return False
            seen.add((r, c))  # mark

            # try all 4 dirs with i+1
            found = (dfs(r + 1, c, i + 1)) or (dfs(r - 1, c, i + 1)) or (dfs(r, c + 1, i + 1)) or (dfs(r, c - 1, i + 1))
            seen.remove((r, c))  # unmark

            return found

        for r in range(rows):
            for c in range(cols):
                if dfs(r, c, 0):
                    return True

        return False


if __name__ == "__main__":
    sol = Solution()
    board = [["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]]
    word = "ABCCED"
    print(sol.exist(board, word))
    board = [["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]]
    word = "SEE"
    print(sol.exist(board, word))
    board = [["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]]
    word = "ABCB"
    print(sol.exist(board, word))
