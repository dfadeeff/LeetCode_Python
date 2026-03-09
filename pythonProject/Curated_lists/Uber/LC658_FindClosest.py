import heapq
from typing import List


class Solution:
    def findClosestElements(self, arr: List[int], k: int, x: int) -> List[int]:
        minheap = []
        for i in arr:
            dist = abs(i - x)
            minheap.append([dist, i])
        heapq.heapify(minheap)

        print(minheap)
        res = []
        while k > 0:
            d, el = heapq.heappop(minheap)
            res.append(el)
            k -= 1
        return sorted(res)


if __name__ == "__main__":
    sol = Solution()

    arr = [1, 2, 3, 4, 5]
    k = 4
    x = 3
    print(sol.findClosestElements(arr, k, x))
