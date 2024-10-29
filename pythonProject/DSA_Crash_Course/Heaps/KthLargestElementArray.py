import heapq
from typing import List


class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        heap = []

        for num in nums:
            heapq.heappush(heap, -num)
        while k > 1:
            k -= 1
            heapq.heappop(heap)


        return -heap[0]


def main():
    nums = [3, 2, 1, 5, 6, 4]
    k = 2
    print(Solution().findKthLargest(nums, k))
    nums = [3, 2, 3, 1, 2, 4, 5, 5, 6]
    k = 4
    print(Solution().findKthLargest(nums, k))


if __name__ == '__main__':
    main()
