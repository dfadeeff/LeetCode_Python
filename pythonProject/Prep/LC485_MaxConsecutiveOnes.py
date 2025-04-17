from typing import List


class Solution:
    def findMaxConsecutiveOnes(self, nums: List[int]) -> int:
        if len(nums) == 1:
            return nums[0]
        currentCount = maxCount = 0
        i = 0
        while i < len(nums):
            if nums[i] == 1:
                currentCount += 1
                maxCount = max(maxCount, currentCount)
            else:
                currentCount = 0
            i+=1

        return maxCount


if __name__ == '__main__':
    nums = [1, 1, 0, 1, 1, 1]
    print(Solution().findMaxConsecutiveOnes(nums))
    nums = [1, 0, 1, 1, 0, 1]
    print(Solution().findMaxConsecutiveOnes(nums))
    nums = [0]
    print(Solution().findMaxConsecutiveOnes(nums))
    nums = [0, 0]
    print(Solution().findMaxConsecutiveOnes(nums))
