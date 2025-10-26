"""
Interview prompt
Tic Tac Toe is a simple two-player game where players take turns marking X or O on a 3×3 grid.
The objective is to be the first to align three of your symbols horizontally, vertically, or
diagonally, upon which you win the game.

Part 1:

Come up with a class TicTacToe that represents a game of tic-tac-toe. Maintain board state, and
design the method execute_move with the below signature.

Note: No AI agent/completion can be used for this phase. Please disable tab completions in your
IDE.
"""
from typing import Literal, Tuple


class TicTacToe:
    def __init__(self, n: int) -> None:
        self.n = n
        self.rows = [0] * n
        self.cols = [0] * n
        self.diag = 0
        self.anti_diag = 0
        self.moves = 0
        self.board = [[None] * n for _ in range(n)]
        self.game_over = False

    def execute_move(
            self, symbol: Literal["X", "O"], row: int, column: int
    ) -> Tuple[bool, Literal["X wins", "O wins", "Draw", "Ongoing"]]:
        """
        Attempts to place the symbol at (x, y).
        Returns (is_valid_move, game_state).
        """
        if self.game_over:
            return False, "invalid move"
        if player not in ("X", "O"):
            return False, "invalid player"
        if not (0 <= row < self.n and 0 <= column < self.n):
            return False, "invalid"
        if self.board[row][column] is not None:
            return False, "invalid"

        add = 1 if player == "X" else -1
        self.board[row][column] = player
        self.rows[row] += add
        self.cols[column] += add
        self.moves += 1

        if row == column:
            self.diag += add
        if row + column == self.n - 1:
            self.anti_diag += add

        # Win condition
        if (abs(self.rows[row]) == self.n or abs(self.cols[column]) == self.n or abs(self.diag) == self.n or abs(
                self.anti_diag) == self.n):
            self.game_over = True
            return True, f"{player} wins"

        # Draw condition
        if self.moves == self.n * self.n:
            self.game_over = True
            return True, "Draw"
        return True, "Ongoing"

    def move(self, row: int, col: int, player: int) -> int:

        if not (0 <= row < self.n or 0 <= col < self.n):
            raise ValueError(f"Invalid move: ({row}, {col}) outside board")

        add = 1 if player == 1 else -1
        self.rows[row] += add
        self.cols[col] += add

        if row == col:
            self.diag += add
        if row + col == self.n - 1:
            self.anti_diag += add

        # check win conditio
        if (abs(self.rows[row]) == self.n or abs(self.cols[col]) == self.n or abs(self.diag) == self.n or abs(
                self.anti_diag) == self.n):
            return player

        return 0


test_cases = [
    [
        ("X", 0, 0),  # True, Ongoing
        ("O", 1, 1),  # True, Ongoing
        ("X", 1, 0),  # True, Ongoing
        ("O", 2, 0),  # True, Ongoing
        ("X", 0, 2),  # True, Ongoing
        ("O", 0, 1),  # True, Ongoing
        ("X", 0, 1),  # False, Ongoing (invalid move)
        ("X", 2, 2),  # True, Ongoing
        ("O", 2, 1)  # True, O wins
    ],
    [
        ("X", 1, 1),  # True, Ongoing
        ("O", 0, 1),  # True, Ongoing
        ("X", 1, 0),  # True, Ongoing
        ("O", 1, 2),  # True, Ongoing
        ("X", 0, 0),  # True, Ongoing
        ("O", 2, 0),  # True, Ongoing
        ("X", 2, 2)  # True, X wins
    ],
    [
        ("X", 0, 0),  # True, Ongoing
        ("O", 0, 1),  # True, Ongoing
        ("X", 0, 2),  # True, Ongoing
        ("O", 1, 1),  # True, Ongoing
        ("X", 1, 0),  # True, Ongoing
        ("O", 1, 2),  # True, Ongoing
        ("X", 2, 1),  # True, Ongoing
        ("O", 2, 0),  # True, Ongoing
        ("X", 2, 2),  # True, Draw
    ],
]

if __name__ == "__main__":
    tictactoe = TicTacToe(3)
    # print(tictactoe.move(0,1,1))
    # print(tictactoe.move(1,1,1))
    # print(tictactoe.move(1,2,2))
    # print(tictactoe.move(1,2,2))

    # for moves in test_cases:
    #    for player, row, col in moves:
    #        result = tictactoe.execute_move(player, row, col)
    #        print(result)
    for i, moves in enumerate(test_cases, 1):
        game = TicTacToe(3)
        print(f"\n--- Game {i} ---")
        for player, row, col in moves:
            valid, state = game.execute_move(player, row, col)
            print(f"{player} -> ({row},{col}) => ({valid}, {state})")
            if state in ("X wins", "O wins", "Draw"):
                break

"""
Part 2:

Once arrived at a working solution, create a Frontend to visualise the state of the board.

Create a backend that allows you to play this game with another player (for this assessment, 
both players play on the same device).

Use the TicTacToe class that you constructed above in the game logic.

You can use any AI tools of your choice for this phase.
"""