import heapq
from collections import Counter
from typing import List


class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        # hashmap
        counts = Counter(nums)
        print(counts)
        heap = []

        # Python has by default min heap, make freq first, since comparison from left to right
        for key, val in counts.items():
            # push tuple (val, key) onto the heap
            heapq.heappush(heap, (val, key))
            if len(heap) > k:
                heapq.heappop(heap)
        return [pair[1] for pair in heap]


def main():
    nums = [1, 1, 1, 2, 2, 3]
    k = 2
    print(Solution().topKFrequent(nums, k))
    nums = [1]
    k = 1
    print(Solution().topKFrequent(nums, k))


if __name__ == '__main__':
    main()
