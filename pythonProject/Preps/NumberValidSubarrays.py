from typing import List


class Solution:
    def validSubarrays(self, nums: List[int]) -> int:
        stack = []
        res = 0
        for i in range(len(nums)):
            while stack and nums[stack[-1]] > nums[i]:
                stack.pop()
            stack.append(i)
            res += len(stack)
        return res


if __name__ == "__main__":
    nums = [1, 4, 2, 5, 3]
    print(Solution().validSubarrays(nums))
