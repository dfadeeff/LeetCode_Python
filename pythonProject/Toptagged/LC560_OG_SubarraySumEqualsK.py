from typing import List
from collections import defaultdict


class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        prefix_sums = defaultdict(int)
        prefix_sums[0] = 1
        res = curSum = 0

        for num in nums:
            curSum += num
            diff = curSum - k
            res += prefix_sums[diff]
            prefix_sums[curSum] += 1

        return res


if __name__ == "__main__":
    nums = [1, 2, 3]
    k = 3
    print(Solution().subarraySum(nums, k))
