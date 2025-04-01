from typing import List


class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        globalMaxSum = float('-inf')
        localMaxSum = float('-inf')
        for i in range(len(nums)):
            localMaxSum = max(nums[i], localMaxSum + nums[i])
            globalMaxSum = max(globalMaxSum, localMaxSum)
        return globalMaxSum

if __name__ == "__main__":
    nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    print(Solution().maxSubArray(nums))
    nums = [5, 4, -1, 7, 8]
    print(Solution().maxSubArray(nums))
