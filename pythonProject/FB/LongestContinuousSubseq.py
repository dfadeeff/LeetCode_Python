from typing import List


class Solution:
    def findLengthOfLCIS(self, nums: List[int]) -> int:
        if len(nums) == 1:
            return 1
        left = curr = ans = 0

        for right in range(1, len(nums)):
            if nums[right] > nums[right - 1]:
                curr += 1
            while nums[right] <= nums[right - 1] and left < right:
                curr -= 1
                left += 1
            ans = max(ans, right - left + 1)

        return ans


if __name__ == "__main__":
    nums = [1, 3, 5, 4, 7]
    print(Solution().findLengthOfLCIS(nums))
    nums = [2, 2, 2, 2, 2]
    print(Solution().findLengthOfLCIS(nums))
    nums = [1]
    print(Solution().findLengthOfLCIS(nums))
