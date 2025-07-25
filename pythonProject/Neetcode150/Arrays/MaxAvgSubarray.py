from typing import List


class Solution:
    def findMaxAverage(self, nums: List[int], k: int) -> float:

        curr, ans = 0, 0
        for i in range(k):
            curr += nums[i]
        ans = curr
        for i in range(k, len(nums)):
            curr += nums[i] - nums[i - k]
            ans = max(ans, curr)

        return ans / k


if __name__ == "__main__":
    nums = [1, 12, -5, -6, 50, 3]
    k = 4
    print(Solution().findMaxAverage(nums, k))
    nums = [5]
    k = 1
    print(Solution().findMaxAverage(nums, k))
