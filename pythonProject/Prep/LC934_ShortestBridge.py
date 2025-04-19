from typing import List
from collections import deque


class Solution:
    def shortestBridge(self, grid: List[List[int]]) -> int:
        n = len(grid)
        # up right down left
        direct = [(-1, 0), (0, 1), (1, 0), (0, -1)]

        def isvalid(r, c):
            return r < 0 or c < 0 or r == n or c == n

        visit = set()

        def dfs(r, c):
            if (isvalid(r, c) or not grid[r][c] or (r, c) in visit):
                return
            visit.add((r, c))
            for dr, dc in direct:
                dfs(r + dr, c + dc)

        def bfs():
            res, queue = 0, deque(visit)
            while queue:
                length = len(queue)
                for _ in range(length):
                    r, c = queue.popleft()
                    for dr, dc in direct:
                        newRow, newCol = r + dr, c + dc
                        if isvalid(newRow, newCol) or (newRow, newCol) in visit:
                            continue
                        if grid[newRow][newCol]:
                            return res
                        queue.append([newRow, newCol])
                        visit.add((newRow, newCol))
                res += 1
        for r in range(n):
            for c in range(n):
                if grid[r][c]:
                    dfs(r, c)
                    return bfs()


if __name__ == "__main__":
    grid = [[0, 1, 0], [0, 0, 0], [0, 0, 1]]
    print(Solution().shortestBridge(grid))
