from typing import List


class Solution:
    def findMissingRanges(self, nums: List[int], lower: int, upper: int) -> List[List[int]]:
        # 1) between 2 numbers
        # 2) missing at the start
        # 3) missing at the end
        n = len(nums)
        missing_ranges = []

        if n == 0:
            return [[lower, upper]]

        if lower < nums[0]:
            missing_ranges.append([lower, nums[0] - 1])

        for i in range(n - 1):
            if nums[i + 1] - nums[i] <= 1:
                continue
            missing_ranges.append([nums[i] + 1, nums[i + 1] - 1])

        # check at the end
        if upper > nums[n - 1]:
            missing_ranges.append([nums[n - 1] + 1, upper])

        return missing_ranges


if __name__ == "__main__":
    nums = [0, 1, 3, 50, 75]
    lower = 0
    upper = 99
    print(Solution().findMissingRanges(nums, lower, upper))
