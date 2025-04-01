from typing import List


class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        globalMaxSum = float('-inf')
        localMaxSum = float('-inf')
        for i in range(0, len(nums)):
            localMaxSum = max(nums[i], localMaxSum + nums[i])
            if localMaxSum > globalMaxSum:
                globalMaxSum = localMaxSum
        return globalMaxSum


if __name__ == "__main__":
    nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    print(Solution().maxSubArray(nums))
