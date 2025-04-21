import heapq
from typing import List
from collections import defaultdict


class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:

        # hashmap
        # counts = Counter(nums)
        counts = defaultdict(int)
        for num in nums:
            counts[num] += 1

        print(counts)
        heap = []

        # Python has by default min heap, make freq first, since comparison from left to right
        for key, val in counts.items():
            # push tuple (val, key) onto the heap
            heapq.heappush(heap, (val, key))
            # always popping off the element with the smallest frequency
            if len(heap) > k:
                heapq.heappop(heap)
        print(heap)
        # return [pair[1] for pair in heap]
        return [val for freq, val in heap]


if __name__ == "__main__":
    nums = [1, 1, 1, 2, 2, 3]
    k = 2
    print(Solution().topKFrequent(nums, k))
