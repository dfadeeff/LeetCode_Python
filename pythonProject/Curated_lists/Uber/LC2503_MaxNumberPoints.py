from typing import List
import heapq

class Solution:
    def maxPoints(self, grid: List[List[int]], queries: List[int]) -> List[int]:
        """
        Sort queries ascending → process cheapest first
        Reuse already-expanded frontier for next query
        """

        m, n = len(grid), len(grid[0])
        DIRS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        # sort queries keeping original index
        # to return answers in original order.
        # e.g. enumerate(queries) = [(0,5), (1,6), (2,2)]
        # sorted by value, key=lambdax x: x[1]  = [(2,2), (0,5), (1,6)]
        sorted_q = sorted(enumerate(queries), key=lambda x: x[1])

        heap = [(grid[0][0], 0, 0)]
        visited = {(0, 0)}
        count = 0
        result = [0] * len(queries)

        for idx, q in sorted_q:
            # expand everything below threshold
            while heap and heap[0][0] < q:
                val, r, c = heapq.heappop(heap)
                count += 1
                for dr, dc in DIRS:
                    nr, nc = r+dr, c+dc
                    if (0<= nr < m and 0<=nc < n) and (nr,nc) not in visited:
                        visited.add((nr,nc))
                        heapq.heappush(heap, (grid[nr][nc], nr, nc))


            result[idx] = count
        return result

if __name__ == "__main__":
    sol = Solution()
    grid = [[1, 2, 3], [2, 5, 7], [3, 5, 1]]
    queries = [5, 6, 2]
    # sorted:  [(2,idx=2), (5,idx=0), (6,idx=1)]
    # Start: heap=[(grid[0][0]=1, 0, 0)]  count=0
    print(sol.maxPoints(grid, queries))
