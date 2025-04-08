from typing import List


class Solution:
    def longestSubarray(self, nums: List[int]) -> int:
        left = count_zeros = ans = 0
        for right in range(len(nums)):
            if nums[right] == 0:
                count_zeros += 1
            while count_zeros > 1:
                if nums[left] == 0:
                    count_zeros -= 1
                # shrink the window
                left += 1
            ans = max(ans, right - left + 1)

        return ans - 1


if __name__ == "__main__":
    nums = [1, 1, 0, 1]
    print(Solution().longestSubarray(nums))
    nums = [0, 1, 1, 1, 0, 1, 1, 0, 1]
    print(Solution().longestSubarray(nums))
