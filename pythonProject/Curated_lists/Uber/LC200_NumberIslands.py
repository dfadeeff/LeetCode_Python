import collections
from typing import List

from sklearn.externals.array_api_compat.numpy.linalg import solve


class Solution:
    def numIslandsBFS(self, grid: List[List[str]]) -> int:
        if not grid:
            return 0
        rows, cols = len(grid), len(grid[0])
        visit = set()
        islands = 0

        def bfs(r, c):
            q = collections.deque()
            visit.add((r, c))
            q.append((r, c))
            directions = [[1, 0], [-1, 0], [0, -1], [0, 1]]
            while q:
                row, col = q.popleft()

                for dr, dc in directions:
                    new_row, new_col = row + dr, col + dc
                    if (new_row in range(rows) and new_col in range(cols) and grid[new_row][new_col] == "1" and (
                            new_row, new_col) not in visit):
                        q.append((new_row, new_col))
                        visit.add((new_row, new_col))

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == "1" and (r, c) not in visit:
                    bfs(r, c)
                    islands += 1
        return islands

    def numIslandsDFS(self, grid: List[List[str]]) -> int:
        """
        Step 1: Is this a graph?
        Yes. Every cell is a node. Every cell connects to its 4 neighbors (up, down, left, right). Connected "1"s form a group — that's a connected component.

        Step 2: What's the question type?
        "How many groups?" → Count the number of DFS/BFS launches.

        Step 3: Visited strategy?
        We can sink the land — change "1" to "0" when we visit. No extra space needed. We're told nothing about preserving the grid, so this is fine.

        Step 4: DFS or BFS?

        Either works. No shortest path needed. DFS is simpler to write.
        :param grid:
        :return:

        """

        count = 0
        for r in range(len(grid)):
            for c in range(len(grid[0])):
                if grid[r][c] == "1":  # found new land!
                    count += 1  # new island
                    self.dfs(grid, r, c)  # sink the whole island
        return count

    def dfs(self, grid, r, c):

        # out of bounds?
        if r < 0 or r >= len(grid) or c < 0 or c >= len(grid[0]):
            return
        # water or already sunk?
        if grid[r][c] != "1":
            return
        # sink this cell
        grid[r][c] = "0"
        # explore all 4 neighbors
        self.dfs(grid, r, c + 1)
        self.dfs(grid, r, c - 1)
        self.dfs(grid, r - 1, c)
        self.dfs(grid, r + 1, c)


if __name__ == "__main__":
    solution = Solution()
    grid = [
        ["0", "1", "1", "1", "0"],
        ["0", "1", "0", "1", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "0", "0", "0"]
    ]
    print(solution.numIslandsBFS(grid))
    print(solution.numIslandsDFS(grid))
    grid = [
        ["1", "1", "0", "0", "1"],
        ["1", "1", "0", "0", "1"],
        ["0", "0", "1", "0", "0"],
        ["0", "0", "0", "1", "1"]
    ]
    print(solution.numIslandsBFS(grid))
    print(solution.numIslandsDFS(grid))
