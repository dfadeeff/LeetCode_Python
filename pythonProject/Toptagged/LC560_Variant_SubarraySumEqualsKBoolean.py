from typing import List
from collections import defaultdict


class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        prefix_sums = defaultdict(int)
        prefix_sums[0] = 1
        print("prefix_count")
        res = 0
        curSum = 0
        for num in nums:
            curSum += num
            print("prefix_sum", curSum)
            res += prefix_sums[curSum-k]
            prefix_sums[curSum] += 1


        print("prefix_count", prefix_sums)
        return res > 0


if __name__ == "__main__":
    nums = [1, 2, 3]
    k = 3
    print(Solution().subarraySum(nums, k))
    nums = [1,4,7]
    k = 3
    print(Solution().subarraySum(nums, k))
