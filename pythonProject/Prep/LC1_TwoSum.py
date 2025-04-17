from typing import List

from collections import defaultdict


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        freq_idx = {x: i for i, x in enumerate(nums)}

        for i in range(len(nums)):
            complement = target - nums[i]
            if complement in freq_idx and freq_idx[complement] != i:
                return [i, freq_idx[complement]]

        return []


if __name__ == "__main__":
    nums = [2, 7, 11, 15]
    target = 9
    print(Solution().twoSum(nums, target))
