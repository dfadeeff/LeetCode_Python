from typing import List


class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        current = maxSoFar = nums[0]
        for i in range(1, len(nums)):
            current = max(nums[i], nums[i] + current)

            maxSoFar = max(maxSoFar, current)
        return maxSoFar


if __name__ == "__main__":
    nums = [2, -3, 4, -2, 2, 1, -1, 4]
    print(Solution().maxSubArray(nums))
