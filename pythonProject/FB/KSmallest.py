import heapq
from typing import List


class Solution:
    def findKthSmallest(self, nums: List[int], k: int) -> int:
        # naive sort by N log N
        # heap N log K
        # quick select o(n), o(1), worst case o(n2)
        # max heap is suboptimal since it will have to put all elements onto heap in O(N log N)
        # min heap is optimal since it will run in O ( N log K )

        max_heap = []

        for num in nums:
            heapq.heappush(max_heap, -num)
            if len(max_heap) > k:
                heapq.heappop(max_heap)

        return -max_heap[0]


if __name__ == '__main__':
    nums = [7, 3, 8, 5, 10, 1]
    k = 3
    print(Solution().findKthSmallest(nums, k))
