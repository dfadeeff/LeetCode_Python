from typing import List


class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        left = ans = curr =  0
        for right in range(len(nums)):
            curr += nums[right]
            ans += 1
            while curr >= target:
                curr -= nums[left]
                left += 1
                ans = min(ans, right - left + 1)

        return ans+1


if __name__ == "__main__":
    target = 7
    nums = [2, 3, 1, 2, 4, 3]
    print(Solution().minSubArrayLen(target, nums))
    target = 4
    nums = [1, 4, 4]
    print(Solution().minSubArrayLen(target, nums))
