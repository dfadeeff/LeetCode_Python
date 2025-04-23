from typing import List


class Solution:
    def findMaxConsecutiveOnes(self, nums: List[int]) -> int:
        left, curr, ans = 0, 0, 0
        for right in range(len(nums)):
            if nums[right] == 0:
                curr += 1
            while curr > 1:
                if nums[left] == 0:
                    curr -= 1
                left += 1
            ans = max(ans, right - left + 1)
        return ans


if __name__ == "__main__":
    nums = [1, 1, 0, 1, 1, 1]
    print(Solution().findMaxConsecutiveOnes(nums))
