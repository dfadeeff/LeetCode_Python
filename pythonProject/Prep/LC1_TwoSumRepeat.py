from typing import List


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        freq = {x: i for i, x in enumerate(nums)}
        for i in range(len(nums)):
            complement = target - nums[i]
            if complement in freq and freq[complement] != i:
                return [i, freq[complement]]


if __name__ == "__main__":
    nums = [2, 7, 11, 15]
    target = 9
    print(Solution().twoSum(nums, target))
