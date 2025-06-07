import heapq
from typing import List

class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        minheap = []
        for x,y in points:
            non_sqrt_distance = x**2 + y**2
            minheap.append([non_sqrt_distance, x, y])

        heapq.heapify(minheap)
        res = []
        while k > 0:
            element = heapq.heappop(minheap)
            res.append(element[1:])
            k -= 1
        return res

if __name__ == "__main__":
    points = [[1, 3], [-2, 2]]
    k = 1
    print(Solution().kClosest(points,k))
