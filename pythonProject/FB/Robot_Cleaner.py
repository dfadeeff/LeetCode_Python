from typing import List, Set, Tuple


class Robot:
    def __init__(self, room: List[List[int]], row: int, col: int):
        self.room = room
        self.row = row
        self.col = col
        self.d = 0  # 0 = up, 1 = right, 2 = down, 3 = left
        self.cleaned = set()
        self.rows = len(room)
        self.cols = len(room[0])

    def move(self) -> bool:
        # direction mapping
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        new_row = self.row + directions[self.d][0]
        new_col = self.col + directions[self.d][1]
        if 0 <= new_row < self.rows and 0 <= new_col < self.cols and self.room[new_row][new_col] == 1:
            self.row = new_row
            self.col = new_col
            return True
        return False

    def turnLeft(self):
        self.d = (self.d - 1) % 4

    def turnRight(self):
        self.d = (self.d + 1) % 4

    def clean(self):
        self.cleaned.add((self.row, self.col))
        print(f"Cleaned: ({self.row}, {self.col})")


class Solution:
    """
    1. Clean current position
    2. For all 4 directions:
    a. If next cell is not visited and move() is successful:
        - Move, mark as visited
        - Recursively clean
        - Backtrack to previous position (to explore other directions)
    b. Rotate to try next direction


    n tiles
    N = number of tiles in a room, M number of obstacles
    T: O(N-M)
    S: O(N-M)
    """

    def cleanRoom(self, robot: 'Robot'):
        visited = set()

        # directions: up, right, down, left, IMPORTANT to go either clockwise or counter clockwise, not in random order since ROBOT moves 90 degrees!!!
        # so it goes UP, RIGHT, DOWN, LEFT
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

        def go_back():
            """
            robot.turnLeft()
            robot.turnLeft()
            robot.move()
            robot.turnLeft()
            robot.turnLeft()
            """
            robot.turnRight()
            robot.turnRight()
            robot.move()
            robot.turnRight()
            robot.turnRight()

        def dfs(row: int, col: int, d: int):
            visited.add((row, col))
            robot.clean()

            for i in range(4):
                new_d = (d + i) % 4
                new_row = row + directions[new_d][0]
                new_col = col + directions[new_d][1]

                if (new_row, new_col) not in visited and robot.move():
                    dfs(new_row, new_col, new_d)
                    go_back()

                robot.turnRight()

        dfs(0, 0, 0)  # start at initial position, facing up


if __name__ == '__main__':
    room = [
        [1, 1, 1, 1, 1, 0, 1, 1],
        [1, 1, 1, 1, 1, 0, 1, 1],
        [1, 0, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1]
    ]
    start_row = 1
    start_col = 3
    robot = Robot(room, start_row, start_col)
    Solution().cleanRoom(robot)

    print("Cleaned cells:", robot.cleaned)
