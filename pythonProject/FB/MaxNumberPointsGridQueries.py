import heapq
from typing import List


class Solution:
    def maxPoints(self, grid: List[List[int]], queries: List[int]) -> List[int]:
        rows, cols = len(grid), len(grid[0])
        q = [(n, i) for i, n in enumerate(queries)]
        print(q)
        q.sort()

        min_heap = [(grid[0][0], 0, 0)]  # min-heap: (cell_value, row, col)
        res = [0] * len(queries)  # final answer
        points = 0  # points accumulated so far
        visited = set([(0, 0)])  # cells already counted

        for limit, index in q:
            while min_heap and min_heap[0][0] < limit:
                val, r, c = heapq.heappop(min_heap)
                points += 1
                neighbors = [[r + 1, c], [r - 1, c], [r, c + 1], [r, c - 1]]
                for nr, nc in neighbors:
                    if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited:
                        heapq.heappush(min_heap, (grid[nr][nc], nr, nc))
                        visited.add((nr, nc))

            res[index] = points
        return res


if __name__ == "__main__":
    grid = [[1, 2, 3], [2, 5, 7], [3, 5, 1]]
    queries = [5, 6, 2]
    print(Solution().maxPoints(grid, queries))
