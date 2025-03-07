from typing import List


class Solution:
    def missingNumber(self, nums: List[int]) -> int:
        range_numbers = len(nums)
        nums.sort()

        answer = 0

        for i in range(0,range_numbers+1):
            if i not in nums:
                answer = i
        return answer


if __name__ == '__main__':
    nums = [3, 0, 1]
    print(Solution().missingNumber(nums))
    nums = [0, 1]
    print(Solution().missingNumber(nums))
