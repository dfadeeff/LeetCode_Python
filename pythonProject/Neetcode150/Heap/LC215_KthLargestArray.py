import heapq
from typing import List


class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        heap = []

        for num in nums:
            heapq.heappush(heap, num)
            if len(heap) > k:
                heapq.heappop(heap)
        return heap[0]


if __name__ == "__main__":
    nums = [2, 3, 1, 5, 4]
    k = 2
    print(Solution().findKthLargest(nums, k))
    nums = [2, 3, 1, 1, 5, 5, 4]
    k = 3
    print(Solution().findKthLargest(nums, k))
