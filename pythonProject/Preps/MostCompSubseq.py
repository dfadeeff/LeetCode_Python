from typing import List


class Solution:
    def mostCompetitive(self, nums: List[int], k: int) -> List[int]:
        stack = []
        n = len(nums)
        for i, num in enumerate(nums):
            while stack and num < stack[-1] and len(stack) + (n - i) > k:
                stack.pop()

            if len(stack) < k:
                stack.append(num)

        return stack


if __name__ == "__main__":
    nums = [3, 5, 2, 6]
    k = 2
    print(Solution().mostCompetitive(nums, k))
