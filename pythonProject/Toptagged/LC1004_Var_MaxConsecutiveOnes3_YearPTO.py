from typing import List


class Solution:
    def longestOnes(self, nums: List[int], k: int) -> int:

        left, curr, ans = 0, 0, 0
        for right in range(len(nums)):
            if nums[right] == "F":
                curr += 1
            while curr > k:
                if nums[left] == "F":
                    curr -= 1
                left += 1
            ans = max(ans, right - left + 1)
        return ans


if __name__ == "__main__":
    days = ["F", "T", "T", "F", "F", "T", "F"]
    k = 2
    print(Solution().longestOnes(days, k))
