from typing import List


class Solution:
    def longestOnes(self, nums: List[int], k: int) -> int:

        left, curr, ans = 0, 0, 0
        for right in range(len(nums)):
            if nums[right] == "W":
                curr += 1
            while curr > k:
                if nums[left] == "W":
                    curr -= 1
                left += 1
            ans = max(ans, right - left + 1)
        return ans


if __name__ == "__main__":
    days = ["W","H","H","W","W","H","W"]
    k = 2
    print(Solution().longestOnes(days, k))
    days = ["W", "W", "W", "H", "H", "W"]
    k = 0
    print(Solution().longestOnes(days, k))

