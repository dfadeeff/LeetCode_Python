import heapq
from collections import Counter
from typing import List


class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        counts = Counter(nums)
        print(counts)
        heap = []

        # Python has by default min heap, make freq first, since comparison from left to right
        for key, val in counts.items():
            print("key, val: ", key, val)
            # push tuple (val, key) onto the heap, this is the most important part, first argument is val followed by key!
            heapq.heappush(heap, (val, key))
            if len(heap) > k:
                heapq.heappop(heap)
        return [pair[1] for pair in heap]


if __name__ == '__main__':
    nums = [1, 2, 2, 3, 3, 3]
    k = 2
    print(Solution().topKFrequent(nums, k))
