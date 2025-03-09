from typing import List


class Solution:
    def runningSum(self, nums: List[int]) -> List[int]:

        prefix = [nums[0]]
        for i in range(1,len(nums)):
            prefix.append(prefix[-1] + nums[i])

        return prefix

if __name__ == '__main__':
    nums = [1, 2, 3, 4]
    print(Solution().runningSum(nums))
