from typing import List


class Solution:
    def numSubarrayProductLessThanK(self, nums: List[int], k: int) -> int:
        if k < 0:
            return 1
        curr = 1
        left = 0
        ans = 0

        for right in range(len(nums)):
            curr *= nums[right]
            while curr >= k :
                curr //= nums[left]
                left += 1
            ans += right - left + 1
        return ans

if __name__ == "__main__":
    nums = [10, 5, 2, 6]
    k = 100
    print(Solution().numSubarrayProductLessThanK(nums, k))
