import heapq
from math import floor
from typing import List


class Solution:
    def minStoneSum(self, piles: List[int], k: int) -> int:
        heap = [-num for num in piles]
        heapq.heapify(heap)


        while k > 0:
            k -= 1
            x = heapq.heappop(heap)
            element = floor(x / 2)
            heapq.heappush(heap, element)

        return -sum(heap)


def main():
    piles = [5, 4, 9]
    k = 2
    print(Solution().minStoneSum(piles, k))


if __name__ == '__main__':
    main()
