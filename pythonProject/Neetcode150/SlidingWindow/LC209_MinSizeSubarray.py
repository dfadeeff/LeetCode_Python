from typing import List


class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        left = 0
        curr = 0
        res = float("inf")
        for right in range(0, len(nums)):

            curr += nums[right]
            while curr >= target:
                res = min(res, right - left + 1)
                curr -= nums[left]
                left += 1


        return 0 if res == float('inf') else res


if __name__ == "__main__":
    target = 7
    nums = [2, 3, 1, 2, 4, 3]
    print(Solution().minSubArrayLen(target, nums))
    target = 4
    nums = [1, 4, 4]
    print(Solution().minSubArrayLen(target, nums))
    target = 11
    nums = [1, 1, 1, 1, 1, 1, 1, 1]
    print(Solution().minSubArrayLen(target, nums))
