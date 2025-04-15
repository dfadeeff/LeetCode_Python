from collections import defaultdict
from typing import List


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        freq = defaultdict(int)
        for i in range(len(nums)):
            freq[nums[i]] = i

        for i in range(len(nums)):
            complement = target - nums[i]
            if complement in freq and freq[complement] != i:
                return [i, freq[complement]]
        return []


if __name__ == '__main__':
    nums = [3, 4, 5, 6]
    target = 7
    print(Solution().twoSum(nums, target))