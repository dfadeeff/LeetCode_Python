import heapq
from typing import List
from xml.sax import parse


class Solution:
    def findClosestElements(self, arr: List[int], k: int, x: int) -> List[int]:
        heap = []
        for num in arr:
            distance = abs(x - num)
            # Python only has min heap, so it is negative to make it max heap
            heapq.heappush(heap, (-distance, -num))
            if len(heap) > k:
                heapq.heappop(heap)

        return sorted([-pair[1] for pair in heap])


def main():
    arr = [1, 2, 3, 4, 5]
    k = 4
    x = 3
    print(Solution().findClosestElements(arr, k, x))
    arr = [1, 1, 2, 3, 4, 5]
    k = 4
    x = -1
    print(Solution().findClosestElements(arr, k, x))


if __name__ == '__main__':
    main()
