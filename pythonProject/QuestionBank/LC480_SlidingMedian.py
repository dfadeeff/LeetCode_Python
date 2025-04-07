import collections
import heapq
from typing import List


class Solution:
    def medianSlidingWindow(self, nums: List[int], k: int) -> List[float]:

        """companion to LC 495 Find Median from Data Stream
        https://leetcode.com/problems/find-median-from-data-stream/description/
        """

        smalls = []
        bigs = nums[:k]
        heapq.heapify(bigs)
        heapq.heapify(smalls)
        while len(smalls) < len(bigs):
            heapq.heappush(smalls, -heapq.heappop(bigs))

        removals = collections.Counter()

        medians = []
        i = k - 1
        while i < len(nums):
            medians.append((bigs[0] - smalls[0]) / 2.0 if k % 2 == 0 else -smalls[0])
            i += 1
            if i == len(nums):
                break
            out_num = nums[i - k]
            in_num = nums[i]
            balance = 0
            balance += -1 if out_num <= -smalls[0] else 1
            removals[out_num] += 1

            if smalls and in_num <= -smalls[0]:
                balance += 1
                heapq.heappush(smalls, -in_num)
            else:
                balance -= 1
                heapq.heappush(bigs, in_num)

            if balance < 0:
                heapq.heappush(smalls, -heapq.heappop(bigs))
                balance += 1
            if balance > 0:
                heapq.heappush(bigs, -heapq.heappop(smalls))
                balance -= 1

            while smalls and removals[-smalls[0]]:
                removals[-smalls[0]] -= 1
                heapq.heappop(smalls)

            while bigs and removals[bigs[0]]:
                removals[bigs[0]] -= 1
                heapq.heappop(bigs)

        return medians

if __name__ == '__main__':
    nums = [1, 3, -1, -3, 5, 3, 6, 7]
    k = 3
    print(Solution().medianSlidingWindow(nums, k))
