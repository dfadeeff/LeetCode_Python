import heapq
from typing import List


class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        # naive sort by N log N
        # heap N log K
        # quick select o(n), o(1), worst case o(n2)
        # max heap is suboptimal since it will have to put all elements onto heap in O(N log N)
        # min heap is optimal since it will run in O ( N log K )

        min_heap = []

        for num in nums:
            heapq.heappush(min_heap, num)
            if len(min_heap) > k:
                heapq.heappop(min_heap)

        return min_heap[0]


if __name__ == '__main__':
    nums = [3, 2, 1, 5, 6, 4]
    k = 2
    print(Solution().findKthLargest(nums, k))
