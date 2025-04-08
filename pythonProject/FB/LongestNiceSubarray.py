from typing import List


class Solution:
    def longestNiceSubarray(self, nums: List[int]) -> int:
        """"
         How to track this for multiple numbers efficiently?

         If you loop through every pair, it’s O(n²).
         But with bitmask, you can just combine all numbers’ bits into one number (mask).
        """

        mask = 0
        left = 0
        ans = 0

        for right in range(len(nums)):
            # While there's overlap, shrink window
            # I’m checking explicitly whether the window is invalid (non-zero overlap), and shrinking the window from the left until there is no overlap
            while mask & nums[right] != 0:
                mask ^= nums[left]  # remove nums[left] from mask
                left += 1
            # Add current number to mask
            mask |= nums[right]
            # Update answer
            ans = max(ans, right - left + 1)

        return ans


if __name__ == '__main__':
    nums = [1, 3, 8, 48, 10]
    print(Solution().longestNiceSubarray(nums))
    nums = [3, 1, 5, 11, 13]
    print(Solution().longestNiceSubarray(nums))
