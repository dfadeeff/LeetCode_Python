from typing import List
from collections import defaultdict


class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        left = curr_sum = res = 0
        for right in range(len(nums)):
            curr_sum += nums[right]
            while curr_sum > k:
                curr_sum -= nums[left]
                left += 1
            if curr_sum == k:
                res += 1
        return res


if __name__ == "__main__":
    nums = [1, 2, 3]
    k = 3
    print(Solution().subarraySum(nums, k))
    nums = [1, 4, 7]
    k = 3
    print(Solution().subarraySum(nums, k))
