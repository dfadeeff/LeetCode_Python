import heapq
from collections import defaultdict
from typing import List


class Solution:

    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        hashmap = defaultdict(int)
        for i in nums:
            hashmap[i] += 1
        print(hashmap)
        heap = []
        for key, value in hashmap.items():
            heapq.heappush(heap, (value, key))
            if len(heap) > k:
                heapq.heappop(heap)
        print(heap)
        return [y for _, y in heap]


if __name__ == "__main__":
    sol = Solution()
    nums = [1, 1, 1, 2, 2, 3]
    k = 2
    print(sol.topKFrequent(nums, k))
    nums = [1, 2, 1, 2, 1, 2, 3, 1, 3, 2]
    k = 2
    print(sol.topKFrequent(nums, k))
