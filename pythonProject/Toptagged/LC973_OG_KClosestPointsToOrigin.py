import heapq
from typing import List


class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        heap = []  # “max‑heap” of size ≤ k which is just a negation of min heap in Python
        for x, y in points:
            # print(pair)
            # dist = (pair[0] ** 2 + pair[1] ** 2) ** 0.5
            dist = (x ** 2 + y ** 2) ** 0.5
            # heapq.heappush(heap, (-dist, (-pair[0], -pair[1])))
            heapq.heappush(heap, (-dist, (-x, -y)))
            if len(heap) > k:
                heapq.heappop(heap)
        print(heap)

        # now heap contains (-4.47213595499958, (2, -4)) a tuple
        # consisting of distance as pair[0] and coordinates as pair[1]
        return [[-x for x in pair[1]] for pair in heap]


if __name__ == "__main__":
    points = [[3, 3], [5, -1], [-2, 4]]
    k = 2
    print(Solution().kClosest(points, k))
    points = [[1, 3], [-2, 2]]
    k = 1
    print(Solution().kClosest(points, k))
