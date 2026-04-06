from typing import List
from collections import deque


class Solution:
    def shortestBridge(self, grid: List[List[int]]) -> int:
        """
        DFS → perfect for "find and mark entire island"
        BFS → perfect for "shortest distance" (level = steps)

        Multi-source BFS from ALL cells of island 1
        = shortest distance from island 1 to island 2

        DFS:
          good at: exploring everything connected
          result:  marks ALL cells of island 1
                   seeds BFS queue with ALL island 1 cells

        BFS:
          good at: shortest distance level by level
          input:   ALL island 1 cells as starting points
          result:  minimum steps to reach island 2

        """
        m, n = len(grid), len(grid[0])
        DIRS = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        queue = deque()

        # Phase 1: DFS to find and mark first island
        def dfs(r, c):
            if r < 0 or r >= m or c < 0 or c >= n:          # out of bounds
                return
            if grid[r][c] != 1:                             # not land → stop
                return
            grid[r][c] = 2                                  # mark visited (was 1)

            """"
            DFS marks island AND simultaneously seeds BFS queue
            Two jobs in one pass:
              job 1: mark entire island as visited (grid=2)
              job 2: add all island cells to BFS queue
            """

            queue.append((r, c))                            # ADD TO BFS QUEUE ← key line
            for dr, dc in DIRS:                             # explore all 4 directions
                dfs(r + dr, c + dc)

        # find first 1 and DFS from it

        found = False
        for r in range(m):
            if found:
                break
            for c in range(n):
                if grid[r][c] == 1:
                    dfs(r, c)
                    found = True
                    break

        # find first 1 and DFS from it
        steps = 0
        while queue:
            for _ in range(len(queue)):
                r, c = queue.popleft()                      # process ONE level
                for dr, dc in DIRS:
                    nr, nc = r + dr, c + dc
                    if not (0 <= nr < m and 0 <= nc < n):
                        continue
                    if grid[nr][nc] == 2:
                        continue  # already visited

                    if grid[nr][nc] == 1:
                        return steps
                    grid[nr][nc] = 2  # mark water as visited
                    queue.append((nr, nc))

            steps += 1

        return -1


if __name__ == "__main__":
    sol = Solution()
    grid = [[0, 1, 0], [0, 0, 0], [0, 0, 1]]
    print(sol.shortestBridge(grid))
