import heapq
from typing import List


class Solution:
    def kthSmallestBruteForce(self, matrix: List[List[int]], k: int) -> int:
        heap = []
        for row in matrix:
            for element in row:
                heapq.heappush(heap,-element)

                if len(heap) > k:
                    heapq.heappop(heap)

        return -heap[0]


if __name__ == "__main__":
    matrix = [[1, 5, 9], [10, 11, 13], [12, 13, 15]]
    k = 8
    print(Solution().kthSmallestBruteForce(matrix, k))
    matrix = [[-5]]
    k = 1
    print(Solution().kthSmallestBruteForce(matrix, k))
