from typing import List


class Solution:
    def findMaxConsecutiveOnes(self, nums: List[int]) -> int:
        maxCount = 0
        curr = 0

        for num in nums:
            if num == 1:
                curr += 1
                maxCount = max(maxCount, curr)
            else:
                curr = 0

        return maxCount


if __name__ == "__main__":
    nums = [1, 1, 0, 1, 1, 1]
    print(Solution().findMaxConsecutiveOnes(nums))
