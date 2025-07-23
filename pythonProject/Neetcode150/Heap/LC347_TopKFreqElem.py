from typing import List
import heapq
from collections import defaultdict


class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        hashmap = defaultdict(int)
        for i in nums:
            hashmap[i] += 1

        print(hashmap)

        heap = []
        for key,value in hashmap.items():
            heapq.heappush(heap,(value,key))
            if len(heap) > k:
                heapq.heappop(heap)

        return [y for x,y in heap]


if __name__ == "__main__":
    nums = [1, 1, 1, 2, 2, 3]
    k = 2
    print(Solution().topKFrequent(nums, k))
