from typing import List


class Solution:
    def longestOnes(self, nums: List[int], k: int) -> int:
        left, ans ,curr = 0,0,0
        for right in range(len(nums)):
            if nums[right] == 0:
                curr += 1
            while curr > k:
                if nums[left] == 0:
                    curr -= 1
                left += 1

            ans = max(ans,right - left + 1)
        return ans

if __name__ == "__main__":
    nums = [1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0]
    k = 2
    print(Solution().longestOnes(nums, k))
