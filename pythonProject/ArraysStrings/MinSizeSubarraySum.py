from typing import List


class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        left, curr = 0, 0
        ans = float('inf')
        for right in range(len(nums)):
            curr += nums[right]

            while curr >= target:
                ans = min(ans, right - left + 1)
                curr -= nums[left]
                left += 1

        return ans if ans != float('inf') else 0


if __name__ == '__main__':
    target = 7
    nums = [2, 3, 1, 2, 4, 3]
    print(Solution().minSubArrayLen(target, nums))
    target = 4
    nums = [1, 4, 4]
    print(Solution().minSubArrayLen(target, nums))
    target = 11
    nums = [1, 1, 1, 1, 1, 1, 1, 1]
    print(Solution().minSubArrayLen(target, nums))
    target = 15
    nums = [5, 1, 3, 5, 10, 7, 4, 9, 2, 8]
    print(Solution().minSubArrayLen(target, nums))
